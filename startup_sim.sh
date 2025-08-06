#!/bin/bash
# ClaudeTeam AI Startup Launcher - Simulator Version

echo "
╔══════════════════════════════════════════════════════╗
║   🚀 ClaudeTeam AI - IoT Startup Simulator 🚀        ║
║                                                       ║
║  Human CEO + 5 AI Agent Simulators                   ║
╚══════════════════════════════════════════════════════╝
"

BASE_DIR="/home/jyjjeon/claudeteam-startup"
cd $BASE_DIR

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

# 디렉토리 구조 생성
echo -e "${BLUE}[SETUP]${NC} 작업 공간 초기화..."
mkdir -p $BASE_DIR/{shared-workspace,agents,infrastructure,ceo-office,logs}
mkdir -p $BASE_DIR/shared-workspace/{tasks,specs,messages,reports,status}
mkdir -p $BASE_DIR/shared-workspace/tasks/{pending,in_progress,completed}

# 실행 권한 부여
chmod +x $BASE_DIR/agents/*.sh
chmod +x $BASE_DIR/agents/*.py
chmod +x $BASE_DIR/ceo-dashboard.py

# 에이전트 시작
echo -e "\n${GREEN}[AGENTS]${NC} AI 에이전트 시뮬레이터 시작...\n"

# tmux 세션 확인 및 정리
tmux kill-server 2>/dev/null

# 에이전트 시뮬레이터 시작
agents=("pm" "hardware" "backend" "frontend" "qa")
for agent in "${agents[@]}"; do
    echo -e "${YELLOW}[START]${NC} Starting $agent agent simulator..."
    
    if command -v tmux &> /dev/null; then
        tmux new-session -d -s "${agent}_claude" "python3 $BASE_DIR/agents/agent_simulator.py $agent"
        echo "  → tmux 세션 '${agent}_claude'에서 실행 중"
    else
        python3 $BASE_DIR/agents/agent_simulator.py $agent > $BASE_DIR/logs/${agent}_claude.log 2>&1 &
        echo "  → 백그라운드 프로세스로 실행 중 (PID: $!)"
    fi
    
    sleep 1
done

echo -e "\n${GREEN}✅ 모든 에이전트 시뮬레이터가 시작되었습니다!${NC}\n"

# 상태 확인
sleep 3
python3 $BASE_DIR/ceo-dashboard.py status

echo -e "\n${YELLOW}[사용 가능한 명령어]${NC}"
echo "  📊 상태 확인: python3 ceo-dashboard.py status"
echo "  📌 작업 할당: python3 ceo-dashboard.py assign <agent> <task>"
echo "  📝 제안서 검토: python3 ceo-dashboard.py proposals"
echo "  🛑 종료: tmux kill-server"
echo ""
echo -e "${BLUE}[팁]${NC} tmux 세션 보기: tmux ls"
echo -e "${BLUE}[팁]${NC} 에이전트 로그 보기: tmux attach -t pm_claude"
echo ""

# 테스트 작업 할당
echo -e "\n${GREEN}[TEST]${NC} 테스트 작업을 할당하시겠습니까? (y/n)"
read -r response
if [ "$response" == "y" ]; then
    python3 $BASE_DIR/ceo-dashboard.py assign pm_claude "Create SmartPlug Pro initial specification"
    python3 $BASE_DIR/ceo-dashboard.py assign backend_claude "Design REST API for device management"
    python3 $BASE_DIR/ceo-dashboard.py assign frontend_claude "Create dashboard mockup"
    echo "✅ 테스트 작업이 할당되었습니다."
fi

echo -e "\n${GREEN}[READY]${NC} ClaudeTeam AI 시뮬레이터가 실행 중입니다! 🚀"