#!/bin/bash
# ClaudeTeam AI Startup Launcher

echo "
╔══════════════════════════════════════════════════════╗
║       🚀 ClaudeTeam AI - IoT Startup System 🚀       ║
║                                                       ║
║  Human CEO + 5 AI Agents = Next-Gen IoT Products     ║
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
NC='\033[0m' # No Color

# 함수: 에이전트 상태 확인
check_agent() {
    local agent=$1
    local color=$2
    echo -e "${color}[CHECK]${NC} $agent 준비 중..."
}

# 함수: 에이전트 시작
start_agent() {
    local agent_name=$1
    local script_path=$2
    local window_title=$3
    
    echo -e "${GREEN}[START]${NC} $window_title 시작..."
    
    # tmux 세션으로 실행 (WSL과 Linux 모두 호환)
    if command -v tmux &> /dev/null; then
        tmux new-session -d -s "$agent_name" "$script_path"
        echo "  → tmux 세션 '$agent_name'에서 실행 중"
    else
        # tmux가 없으면 백그라운드로 실행
        nohup "$script_path" > "$BASE_DIR/logs/${agent_name}.log" 2>&1 &
        echo "  → 백그라운드 프로세스로 실행 중 (PID: $!)"
    fi
}

# 옵션 파싱
MODE="full"
if [ "$1" == "--help" ] || [ "$1" == "-h" ]; then
    echo "사용법: ./startup.sh [옵션]"
    echo ""
    echo "옵션:"
    echo "  --full          전체 시스템 시작 (기본값)"
    echo "  --agents-only   에이전트만 시작"
    echo "  --mcp-only      MCP 서버만 시작"
    echo "  --status        상태 확인만"
    echo "  --stop          모든 프로세스 중지"
    echo ""
    exit 0
fi

if [ "$1" != "" ]; then
    MODE=$1
fi

# 디렉토리 구조 생성
echo -e "${BLUE}[SETUP]${NC} 작업 공간 초기화..."
mkdir -p $BASE_DIR/{shared-workspace,agents,infrastructure,ceo-office}
mkdir -p $BASE_DIR/shared-workspace/{tasks,specs,messages,reports,status}
mkdir -p $BASE_DIR/shared-workspace/tasks/{pending,in_progress,completed}

# 실행 권한 부여
chmod +x $BASE_DIR/agents/*.sh
chmod +x $BASE_DIR/infrastructure/*.py
chmod +x $BASE_DIR/ceo-dashboard.py

case $MODE in
    "--stop")
        echo -e "${RED}[STOP]${NC} 모든 프로세스 중지..."
        tmux kill-server 2>/dev/null
        pkill -f "mcp_server.py"
        pkill -f "claude"
        echo "✅ 모든 프로세스가 중지되었습니다."
        ;;
    
    "--status")
        echo -e "${YELLOW}[STATUS]${NC} 시스템 상태 확인..."
        python3 $BASE_DIR/ceo-dashboard.py status
        ;;
    
    "--mcp-only")
        echo -e "${PURPLE}[MCP]${NC} MCP 서버 시작..."
        python3 $BASE_DIR/infrastructure/mcp_server.py &
        echo "✅ MCP 서버가 백그라운드에서 실행 중입니다."
        ;;
    
    "--agents-only"|"--full")
        # MCP 서버 시작
        if [ "$MODE" == "--full" ]; then
            echo -e "${PURPLE}[MCP]${NC} MCP 서버 시작..."
            python3 $BASE_DIR/infrastructure/mcp_server.py &
            MCP_PID=$!
            sleep 2
        fi
        
        # 에이전트 시작
        echo -e "\n${GREEN}[AGENTS]${NC} AI 에이전트 팀 시작...\n"
        
        # PM Claude
        check_agent "PM Claude" "$YELLOW"
        start_agent "pm_claude" "$BASE_DIR/agents/pm_claude.sh" "PM Claude - Product Manager"
        sleep 1
        
        # Hardware Claude
        check_agent "Hardware Claude" "$RED"
        start_agent "hardware_claude" "$BASE_DIR/agents/hardware_claude.sh" "Hardware Claude - HW Engineer"
        sleep 1
        
        # Backend Claude
        check_agent "Backend Claude" "$BLUE"
        start_agent "backend_claude" "$BASE_DIR/agents/backend_claude.sh" "Backend Claude - Server Dev"
        sleep 1
        
        # Frontend Claude
        check_agent "Frontend Claude" "$GREEN"
        start_agent "frontend_claude" "$BASE_DIR/agents/frontend_claude.sh" "Frontend Claude - UI/UX Dev"
        sleep 1
        
        # QA Claude
        check_agent "QA Claude" "$PURPLE"
        start_agent "qa_claude" "$BASE_DIR/agents/qa_claude.sh" "QA Claude - Quality Assurance"
        
        echo -e "\n${GREEN}✅ 모든 에이전트가 시작되었습니다!${NC}\n"
        
        # CEO 대시보드 표시
        sleep 3
        echo "════════════════════════════════════════════════════════"
        python3 $BASE_DIR/ceo-dashboard.py status
        
        echo -e "\n${YELLOW}[CEO 명령어]${NC}"
        echo "  📊 상태 확인: ./ceo-dashboard.py status"
        echo "  📝 제안서 검토: ./ceo-dashboard.py proposals"
        echo "  📌 작업 할당: ./ceo-dashboard.py assign <agent> <task>"
        echo "  💬 메시지: ./ceo-dashboard.py message <agent> <message>"
        echo "  🚨 긴급 회의: ./ceo-dashboard.py meeting <topic>"
        echo ""
        echo -e "${BLUE}[팁]${NC} tmux 세션 확인: tmux ls"
        echo -e "${BLUE}[팁]${NC} tmux 세션 연결: tmux attach -t <agent_name>"
        echo ""
        
        # 첫 작업 시작
        echo -e "\n${GREEN}[START]${NC} 첫 제품 기획을 시작하시겠습니까? (y/n)"
        read -r response
        if [ "$response" == "y" ]; then
            python3 $BASE_DIR/ceo-dashboard.py message pm_claude "스마트홈 IoT 제품 3개를 기획해주세요. 각 제품의 시장성, 기술적 타당성, 예상 개발 기간을 포함해주세요."
            echo "✅ PM Claude에게 제품 기획을 요청했습니다."
        fi
        ;;
    
    *)
        echo "잘못된 옵션입니다. --help로 사용법을 확인하세요."
        ;;
esac

echo -e "\n${GREEN}[READY]${NC} ClaudeTeam AI 스타트업 시스템이 준비되었습니다! 🚀"