#!/usr/bin/env python3
"""
ClaudeTeam MCP Server - 에이전트 간 통신 및 작업 관리
"""

import json
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import redis.asyncio as redis

@dataclass
class Task:
    id: str
    type: str  # "pm", "hardware", "backend", "frontend", "qa"
    title: str
    description: str
    assigned_to: str
    created_by: str
    status: str  # "pending", "in_progress", "review", "completed"
    priority: int  # 1-5
    created_at: str
    updated_at: str
    
@dataclass
class Message:
    from_agent: str
    to_agent: str
    subject: str
    content: str
    timestamp: str
    requires_ceo_approval: bool = False

class SharedWorkspaceMCP:
    def __init__(self):
        self.workspace_dir = Path("/home/jyjjeon/claudeteam-startup/shared-workspace")
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        
        # 디렉토리 구조 생성
        (self.workspace_dir / "tasks" / "pending").mkdir(parents=True, exist_ok=True)
        (self.workspace_dir / "tasks" / "in_progress").mkdir(parents=True, exist_ok=True)
        (self.workspace_dir / "tasks" / "completed").mkdir(parents=True, exist_ok=True)
        (self.workspace_dir / "messages").mkdir(parents=True, exist_ok=True)
        (self.workspace_dir / "specs").mkdir(parents=True, exist_ok=True)
        (self.workspace_dir / "reports").mkdir(parents=True, exist_ok=True)
        
        # Redis for real-time communication (optional)
        self.redis_client = None
        
    async def connect_redis(self):
        """Redis 연결 (실시간 통신용)"""
        try:
            self.redis_client = await redis.from_url("redis://localhost")
            await self.redis_client.ping()
            print("Redis connected for real-time communication")
        except:
            print("Redis not available, using file-based communication")
    
    # ===== Task Management =====
    
    async def create_task(self, task: Task) -> str:
        """새 작업 생성"""
        task_file = self.workspace_dir / "tasks" / "pending" / f"{task.id}.json"
        task_file.write_text(json.dumps(asdict(task), indent=2))
        
        # Redis pub/sub로 알림
        if self.redis_client:
            await self.redis_client.publish(
                f"agent:{task.assigned_to}",
                json.dumps({"type": "new_task", "task_id": task.id})
            )
        
        return task.id
    
    async def get_agent_tasks(self, agent_name: str) -> List[Task]:
        """특정 에이전트의 작업 목록 조회"""
        all_tasks = []
        
        for status_dir in ["pending", "in_progress", "review"]:
            task_dir = self.workspace_dir / "tasks" / status_dir
            for task_file in task_dir.glob("*.json"):
                task_data = json.loads(task_file.read_text())
                if task_data["assigned_to"] == agent_name:
                    all_tasks.append(Task(**task_data))
        
        return sorted(all_tasks, key=lambda x: x.priority, reverse=True)
    
    async def update_task_status(self, task_id: str, new_status: str, agent_name: str):
        """작업 상태 업데이트"""
        # 현재 작업 찾기
        current_task = None
        current_path = None
        
        for status in ["pending", "in_progress", "review", "completed"]:
            path = self.workspace_dir / "tasks" / status / f"{task_id}.json"
            if path.exists():
                current_task = json.loads(path.read_text())
                current_path = path
                break
        
        if not current_task:
            raise ValueError(f"Task {task_id} not found")
        
        # 권한 확인
        if current_task["assigned_to"] != agent_name and agent_name != "ceo":
            raise PermissionError(f"{agent_name} cannot update task assigned to {current_task['assigned_to']}")
        
        # 상태 업데이트
        current_task["status"] = new_status
        current_task["updated_at"] = datetime.now().isoformat()
        
        # 새 위치로 이동
        new_path = self.workspace_dir / "tasks" / new_status / f"{task_id}.json"
        new_path.write_text(json.dumps(current_task, indent=2))
        current_path.unlink()
        
        # CEO에게 알림 (중요 상태 변경시)
        if new_status in ["completed", "blocked"]:
            await self.notify_ceo(f"Task {task_id} is now {new_status}")
    
    # ===== Inter-Agent Communication =====
    
    async def send_message(self, message: Message):
        """에이전트 간 메시지 전송"""
        msg_file = self.workspace_dir / "messages" / f"{message.to_agent}_{message.timestamp}.json"
        msg_file.write_text(json.dumps(asdict(message), indent=2))
        
        # CEO 승인 필요시 별도 처리
        if message.requires_ceo_approval:
            approval_file = self.workspace_dir / "ceo-office" / "inbox" / f"approval_{message.timestamp}.json"
            approval_file.parent.mkdir(parents=True, exist_ok=True)
            approval_file.write_text(json.dumps(asdict(message), indent=2))
        
        # Redis로 실시간 알림
        if self.redis_client:
            await self.redis_client.publish(
                f"agent:{message.to_agent}",
                json.dumps({"type": "new_message", "from": message.from_agent})
            )
    
    async def get_messages(self, agent_name: str) -> List[Message]:
        """에이전트의 메시지 조회"""
        messages = []
        msg_dir = self.workspace_dir / "messages"
        
        for msg_file in msg_dir.glob(f"{agent_name}_*.json"):
            msg_data = json.loads(msg_file.read_text())
            messages.append(Message(**msg_data))
            # 읽은 메시지는 삭제 (또는 archived로 이동)
            msg_file.unlink()
        
        return sorted(messages, key=lambda x: x.timestamp)
    
    # ===== Product Specs Management =====
    
    async def save_product_spec(self, product_name: str, spec: Dict):
        """제품 스펙 저장"""
        spec_file = self.workspace_dir / "specs" / f"{product_name}.json"
        spec["updated_at"] = datetime.now().isoformat()
        spec_file.write_text(json.dumps(spec, indent=2))
        
        # 모든 에이전트에게 스펙 업데이트 알림
        if self.redis_client:
            await self.redis_client.publish(
                "broadcast",
                json.dumps({"type": "spec_update", "product": product_name})
            )
    
    async def get_product_spec(self, product_name: str) -> Dict:
        """제품 스펙 조회"""
        spec_file = self.workspace_dir / "specs" / f"{product_name}.json"
        if spec_file.exists():
            return json.loads(spec_file.read_text())
        return None
    
    # ===== Status & Reporting =====
    
    async def update_agent_status(self, agent_name: str, status: Dict):
        """에이전트 상태 업데이트"""
        status_file = self.workspace_dir / "status" / f"{agent_name}.json"
        status_file.parent.mkdir(exist_ok=True)
        status["timestamp"] = datetime.now().isoformat()
        status_file.write_text(json.dumps(status, indent=2))
    
    async def get_team_status(self) -> Dict:
        """전체 팀 상태 조회"""
        team_status = {}
        status_dir = self.workspace_dir / "status"
        
        if status_dir.exists():
            for status_file in status_dir.glob("*.json"):
                agent_name = status_file.stem
                team_status[agent_name] = json.loads(status_file.read_text())
        
        return team_status
    
    async def generate_daily_report(self) -> Dict:
        """일일 보고서 생성"""
        report = {
            "date": datetime.now().date().isoformat(),
            "tasks": {
                "completed_today": [],
                "in_progress": [],
                "blocked": [],
                "pending_high_priority": []
            },
            "team_status": await self.get_team_status(),
            "ceo_decisions_needed": []
        }
        
        # 작업 상태 집계
        for status in ["completed", "in_progress", "pending"]:
            task_dir = self.workspace_dir / "tasks" / status
            for task_file in task_dir.glob("*.json"):
                task = json.loads(task_file.read_text())
                if status == "completed" and task["updated_at"].startswith(datetime.now().date().isoformat()):
                    report["tasks"]["completed_today"].append(task)
                elif status == "in_progress":
                    report["tasks"]["in_progress"].append(task)
                elif status == "pending" and task["priority"] >= 4:
                    report["tasks"]["pending_high_priority"].append(task)
        
        # CEO 결정 대기 사항
        inbox_dir = self.workspace_dir / "ceo-office" / "inbox"
        if inbox_dir.exists():
            for approval_file in inbox_dir.glob("*.json"):
                report["ceo_decisions_needed"].append(json.loads(approval_file.read_text()))
        
        # 보고서 저장
        report_file = self.workspace_dir / "reports" / f"daily_{datetime.now().date()}.json"
        report_file.write_text(json.dumps(report, indent=2))
        
        return report
    
    # ===== CEO Interface =====
    
    async def notify_ceo(self, message: str, priority: str = "info"):
        """CEO에게 알림"""
        notification = {
            "timestamp": datetime.now().isoformat(),
            "priority": priority,  # "critical", "high", "normal", "info"
            "message": message
        }
        
        notif_file = self.workspace_dir / "ceo-office" / "notifications" / f"{datetime.now().timestamp()}.json"
        notif_file.parent.mkdir(parents=True, exist_ok=True)
        notif_file.write_text(json.dumps(notification, indent=2))
        
        if self.redis_client and priority in ["critical", "high"]:
            await self.redis_client.publish("ceo:urgent", json.dumps(notification))

# MCP Server Runner
async def run_mcp_server():
    """MCP 서버 실행"""
    server = SharedWorkspaceMCP()
    await server.connect_redis()
    
    print("🚀 ClaudeTeam MCP Server Started")
    print("📁 Workspace: /home/jyjjeon/claudeteam-startup/shared-workspace")
    print("⏰ Monitoring agent activities...")
    
    # 주기적으로 일일 보고서 생성 (실제로는 스케줄러 사용)
    while True:
        await asyncio.sleep(3600)  # 1시간마다
        # 오후 6시에 일일 보고서 생성
        if datetime.now().hour == 18:
            report = await server.generate_daily_report()
            await server.notify_ceo("Daily report generated", "normal")

if __name__ == "__main__":
    asyncio.run(run_mcp_server())