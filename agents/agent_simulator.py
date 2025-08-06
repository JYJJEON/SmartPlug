#!/usr/bin/env python3
"""
AI Agent Simulator - 실제 Claude 대신 시뮬레이션 동작
"""

import json
import time
import sys
from pathlib import Path
from datetime import datetime
import random

class AgentSimulator:
    def __init__(self, agent_type):
        self.agent_type = agent_type
        self.base_dir = Path("/home/jyjjeon/claudeteam-startup")
        self.shared_dir = self.base_dir / "shared-workspace"
        self.workspace = self.base_dir / f"{agent_type}-workspace"
        self.workspace.mkdir(parents=True, exist_ok=True)
        
        # 에이전트별 동작 정의
        self.agent_behaviors = {
            "pm": self.pm_behavior,
            "hardware": self.hardware_behavior,
            "backend": self.backend_behavior,
            "frontend": self.frontend_behavior,
            "qa": self.qa_behavior
        }
    
    def run(self):
        """에이전트 실행"""
        print(f"[{self.agent_type.upper()}] Agent started at {datetime.now()}")
        
        # 상태 업데이트
        self.update_status("Initializing")
        
        # 작업 확인 및 수행 루프
        while True:
            try:
                # 작업 확인
                tasks = self.get_pending_tasks()
                
                if tasks:
                    task = tasks[0]  # 우선순위가 가장 높은 작업
                    self.process_task(task)
                else:
                    # 에이전트별 자율 동작
                    if self.agent_type in self.agent_behaviors:
                        self.agent_behaviors[self.agent_type]()
                    else:
                        self.update_status("Idle")
                
                time.sleep(10)  # 10초마다 체크
                
            except KeyboardInterrupt:
                print(f"[{self.agent_type.upper()}] Shutting down...")
                break
            except Exception as e:
                print(f"[{self.agent_type.upper()}] Error: {e}")
                time.sleep(5)
    
    def get_pending_tasks(self):
        """대기 중인 작업 조회"""
        tasks = []
        pending_dir = self.shared_dir / "tasks" / "pending"
        
        if pending_dir.exists():
            for task_file in pending_dir.glob("*.json"):
                task = json.loads(task_file.read_text())
                if task.get("assigned_to") == f"{self.agent_type}_claude":
                    tasks.append(task)
        
        return sorted(tasks, key=lambda x: x.get("priority", 0), reverse=True)
    
    def process_task(self, task):
        """작업 처리"""
        task_id = task["id"]
        print(f"[{self.agent_type.upper()}] Processing task: {task['title']}")
        
        # 작업을 진행 중으로 이동
        self.move_task(task_id, "pending", "in_progress")
        self.update_status(f"Working on: {task['title']}")
        
        # 작업 시뮬레이션 (5-15초)
        work_time = random.randint(5, 15)
        time.sleep(work_time)
        
        # 작업 완료
        self.move_task(task_id, "in_progress", "completed")
        self.update_status("Task completed")
        
        # 결과 리포트 생성
        self.create_task_report(task)
    
    def move_task(self, task_id, from_status, to_status):
        """작업 상태 변경"""
        from_path = self.shared_dir / "tasks" / from_status / f"{task_id}.json"
        to_path = self.shared_dir / "tasks" / to_status / f"{task_id}.json"
        
        if from_path.exists():
            task = json.loads(from_path.read_text())
            task["status"] = to_status
            task["updated_at"] = datetime.now().isoformat()
            
            to_path.parent.mkdir(parents=True, exist_ok=True)
            to_path.write_text(json.dumps(task, indent=2))
            from_path.unlink()
    
    def update_status(self, status_text):
        """에이전트 상태 업데이트"""
        status = {
            "agent": f"{self.agent_type}_claude",
            "current_task": status_text,
            "timestamp": datetime.now().isoformat()
        }
        
        status_dir = self.shared_dir / "status"
        status_dir.mkdir(parents=True, exist_ok=True)
        status_file = status_dir / f"{self.agent_type}_claude.json"
        status_file.write_text(json.dumps(status, indent=2))
    
    def create_task_report(self, task):
        """작업 완료 리포트 생성"""
        report = {
            "task_id": task["id"],
            "task_title": task["title"],
            "completed_by": f"{self.agent_type}_claude",
            "completed_at": datetime.now().isoformat(),
            "results": f"Successfully completed {task['title']}"
        }
        
        reports_dir = self.shared_dir / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        report_file = reports_dir / f"{task['id']}_report.json"
        report_file.write_text(json.dumps(report, indent=2))
    
    # === 에이전트별 특수 동작 ===
    
    def pm_behavior(self):
        """PM 에이전트 자율 동작"""
        if random.random() < 0.3:  # 30% 확률로 제안서 생성
            self.create_product_proposal()
        else:
            self.update_status("Market research")
    
    def create_product_proposal(self):
        """제품 제안서 생성"""
        products = ["Smart Lock", "Pet Tracker", "Plant Monitor", "Energy Meter"]
        product = random.choice(products)
        
        proposal = {
            "product_name": product,
            "category": "IoT/SmartHome",
            "target_customer": "Tech-savvy homeowners",
            "price": f"₩{random.randint(30, 100)*1000:,}",
            "development_time": f"{random.randint(4, 12)} weeks",
            "created_at": datetime.now().isoformat()
        }
        
        proposals_dir = self.base_dir / "pm-workspace" / "proposals"
        proposals_dir.mkdir(parents=True, exist_ok=True)
        proposal_file = proposals_dir / f"{product.lower().replace(' ', '_')}.json"
        proposal_file.write_text(json.dumps(proposal, indent=2))
        
        print(f"[PM] Created proposal for {product}")
        self.update_status(f"Created proposal: {product}")
    
    def hardware_behavior(self):
        """Hardware 에이전트 자율 동작"""
        self.update_status("PCB design optimization")
    
    def backend_behavior(self):
        """Backend 에이전트 자율 동작"""
        self.update_status("API development")
    
    def frontend_behavior(self):
        """Frontend 에이전트 자율 동작"""
        self.update_status("UI/UX improvements")
    
    def qa_behavior(self):
        """QA 에이전트 자율 동작"""
        self.update_status("Running tests")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        agent_type = sys.argv[1]
        simulator = AgentSimulator(agent_type)
        simulator.run()
    else:
        print("Usage: agent_simulator.py <agent_type>")
        print("Agent types: pm, hardware, backend, frontend, qa")