#!/usr/bin/env python3
"""
CEO Dashboard - ClaudeTeam AI 스타트업 관리 인터페이스
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import subprocess

class CEODashboard:
    def __init__(self):
        self.base_dir = Path("/home/jyjjeon/claudeteam-startup")
        self.shared_dir = self.base_dir / "shared-workspace"
        self.ceo_dir = self.base_dir / "ceo-office"
        
        # CEO 디렉토리 생성
        (self.ceo_dir / "inbox").mkdir(parents=True, exist_ok=True)
        (self.ceo_dir / "reports").mkdir(parents=True, exist_ok=True)
        (self.ceo_dir / "approvals").mkdir(parents=True, exist_ok=True)
        (self.ceo_dir / "decisions").mkdir(parents=True, exist_ok=True)
    
    def show_status(self):
        """전체 상태 요약"""
        print("\n" + "="*60)
        print("🏢 ClaudeTeam AI - CEO Dashboard")
        print("="*60)
        
        # 팀 상태
        print("\n📊 팀 상태:")
        status_dir = self.shared_dir / "status"
        if status_dir.exists():
            for status_file in status_dir.glob("*.json"):
                agent = status_file.stem
                data = json.loads(status_file.read_text())
                print(f"  • {agent}: {data.get('current_task', 'Idle')}")
        
        # 작업 현황
        print("\n📋 작업 현황:")
        for status in ["pending", "in_progress", "completed"]:
            task_count = len(list((self.shared_dir / "tasks" / status).glob("*.json")))
            print(f"  • {status.capitalize()}: {task_count}")
        
        # 승인 대기
        print("\n⏳ 승인 대기 사항:")
        inbox = self.ceo_dir / "inbox"
        if inbox.exists():
            approvals = list(inbox.glob("*.json"))
            if approvals:
                for approval_file in approvals[:3]:  # 최대 3개만 표시
                    data = json.loads(approval_file.read_text())
                    print(f"  • {data.get('subject', 'Unknown')}")
            else:
                print("  • 없음")
        
        print("\n" + "="*60)
    
    def review_proposals(self):
        """제품 제안서 검토"""
        proposals_dir = self.base_dir / "pm-workspace" / "proposals"
        proposals_dir.mkdir(parents=True, exist_ok=True)
        
        print("\n📝 제품 제안서:")
        proposals = list(proposals_dir.glob("*.json"))
        
        if not proposals:
            print("  현재 검토할 제안서가 없습니다.")
            return
        
        for idx, proposal_file in enumerate(proposals, 1):
            proposal = json.loads(proposal_file.read_text())
            print(f"\n  [{idx}] {proposal.get('product_name', 'Unknown')}")
            print(f"      타겟: {proposal.get('target_customer', 'N/A')}")
            print(f"      예상 가격: {proposal.get('price', 'N/A')}")
            print(f"      개발 기간: {proposal.get('development_time', 'N/A')}")
        
        choice = input("\n검토할 제안서 번호 (0: 취소): ")
        if choice != "0" and choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(proposals):
                self._review_proposal(proposals[idx])
    
    def _review_proposal(self, proposal_file: Path):
        """특정 제안서 상세 검토"""
        proposal = json.loads(proposal_file.read_text())
        
        print("\n" + "="*50)
        print(f"제품명: {proposal.get('product_name')}")
        print(f"카테고리: {proposal.get('category')}")
        print(f"타겟 고객: {proposal.get('target_customer')}")
        print(f"핵심 문제: {proposal.get('core_problem')}")
        print(f"솔루션: {proposal.get('solution')}")
        print(f"차별화: {proposal.get('differentiation')}")
        print(f"MVP 기능: {proposal.get('mvp_features')}")
        print(f"예상 가격: {proposal.get('price')}")
        print(f"개발 기간: {proposal.get('development_time')}")
        print(f"예상 BEP: {proposal.get('break_even_point')}")
        print("="*50)
        
        decision = input("\n결정 (approve/reject/modify): ").lower()
        
        if decision == "approve":
            self._approve_proposal(proposal)
            print("✅ 제안서가 승인되었습니다.")
        elif decision == "reject":
            reason = input("반려 사유: ")
            self._reject_proposal(proposal, reason)
            print("❌ 제안서가 반려되었습니다.")
        elif decision == "modify":
            feedback = input("수정 요청 사항: ")
            self._request_modification(proposal, feedback)
            print("📝 수정 요청이 전달되었습니다.")
    
    def _approve_proposal(self, proposal: Dict):
        """제안서 승인"""
        approval = {
            "product_name": proposal.get("product_name"),
            "approved_at": datetime.now().isoformat(),
            "status": "approved",
            "next_steps": "개발 착수"
        }
        
        approval_file = self.ceo_dir / "approvals" / f"{proposal.get('product_name')}_{datetime.now().timestamp()}.json"
        approval_file.write_text(json.dumps(approval, indent=2))
        
        # PM에게 작업 할당
        self._assign_task("pm_claude", f"Start development of {proposal.get('product_name')}", priority=5)
    
    def _reject_proposal(self, proposal: Dict, reason: str):
        """제안서 반려"""
        rejection = {
            "product_name": proposal.get("product_name"),
            "rejected_at": datetime.now().isoformat(),
            "status": "rejected",
            "reason": reason
        }
        
        decision_file = self.ceo_dir / "decisions" / f"reject_{datetime.now().timestamp()}.json"
        decision_file.write_text(json.dumps(rejection, indent=2))
    
    def _request_modification(self, proposal: Dict, feedback: str):
        """수정 요청"""
        modification = {
            "product_name": proposal.get("product_name"),
            "requested_at": datetime.now().isoformat(),
            "status": "modification_requested",
            "feedback": feedback
        }
        
        decision_file = self.ceo_dir / "decisions" / f"modify_{datetime.now().timestamp()}.json"
        decision_file.write_text(json.dumps(modification, indent=2))
        
        # PM에게 수정 작업 할당
        self._assign_task("pm_claude", f"Modify proposal: {feedback}", priority=4)
    
    def assign_task(self, agent: str, task_description: str):
        """특정 에이전트에게 작업 할당"""
        self._assign_task(agent, task_description, priority=3)
        print(f"✅ {agent}에게 작업이 할당되었습니다.")
    
    def _assign_task(self, agent: str, description: str, priority: int = 3):
        """작업 생성 및 할당"""
        task = {
            "id": f"task_{datetime.now().timestamp()}",
            "type": agent.split("_")[0],  # pm, hardware, backend, frontend, qa
            "title": description.split(":")[0] if ":" in description else description[:50],
            "description": description,
            "assigned_to": agent,
            "created_by": "ceo",
            "status": "pending",
            "priority": priority,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        task_file = self.shared_dir / "tasks" / "pending" / f"{task['id']}.json"
        task_file.parent.mkdir(parents=True, exist_ok=True)
        task_file.write_text(json.dumps(task, indent=2))
    
    def view_reports(self):
        """보고서 보기"""
        reports_dir = self.shared_dir / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        print("\n📊 최근 보고서:")
        reports = sorted(reports_dir.glob("*.json"), reverse=True)[:5]
        
        for report_file in reports:
            report = json.loads(report_file.read_text())
            print(f"  • {report_file.stem}: {report.get('date', 'N/A')}")
    
    def send_message(self, agent: str, message: str):
        """에이전트에게 메시지 전송"""
        msg = {
            "from_agent": "ceo",
            "to_agent": agent,
            "subject": message[:50],
            "content": message,
            "timestamp": datetime.now().isoformat(),
            "requires_ceo_approval": False
        }
        
        msg_file = self.shared_dir / "messages" / f"{agent}_{datetime.now().timestamp()}.json"
        msg_file.parent.mkdir(parents=True, exist_ok=True)
        msg_file.write_text(json.dumps(msg, indent=2))
        
        print(f"✉️ {agent}에게 메시지를 전송했습니다.")
    
    def emergency_meeting(self, topic: str):
        """긴급 회의 소집"""
        print(f"\n🚨 긴급 회의 소집: {topic}")
        
        agents = ["pm_claude", "hardware_claude", "backend_claude", "frontend_claude", "qa_claude"]
        for agent in agents:
            self.send_message(agent, f"URGENT MEETING: {topic}. Please review and prepare your status.")
        
        print("모든 에이전트에게 긴급 회의 알림을 전송했습니다.")

def main():
    dashboard = CEODashboard()
    
    if len(sys.argv) < 2:
        dashboard.show_status()
        print("\n사용법:")
        print("  ./ceo-dashboard.py status          - 전체 상태 확인")
        print("  ./ceo-dashboard.py proposals       - 제품 제안서 검토")
        print("  ./ceo-dashboard.py assign <agent> <task> - 작업 할당")
        print("  ./ceo-dashboard.py message <agent> <msg> - 메시지 전송")
        print("  ./ceo-dashboard.py meeting <topic> - 긴급 회의")
        print("  ./ceo-dashboard.py reports         - 보고서 보기")
        return
    
    command = sys.argv[1]
    
    if command == "status":
        dashboard.show_status()
    elif command == "proposals":
        dashboard.review_proposals()
    elif command == "assign" and len(sys.argv) >= 4:
        agent = sys.argv[2]
        task = " ".join(sys.argv[3:])
        dashboard.assign_task(agent, task)
    elif command == "message" and len(sys.argv) >= 4:
        agent = sys.argv[2]
        message = " ".join(sys.argv[3:])
        dashboard.send_message(agent, message)
    elif command == "meeting" and len(sys.argv) >= 3:
        topic = " ".join(sys.argv[2:])
        dashboard.emergency_meeting(topic)
    elif command == "reports":
        dashboard.view_reports()
    else:
        print("잘못된 명령입니다.")

if __name__ == "__main__":
    main()