#!/bin/bash
# Git Worktree Setup for Multi-Agent Collaboration

echo "
╔══════════════════════════════════════════════════════╗
║     Git Worktree Setup for ClaudeTeam AI Agents      ║
╚══════════════════════════════════════════════════════╝
"

BASE_DIR="/home/jyjjeon/claudeteam-startup"
PROJECT_NAME="smartplug-pro"
GIT_REPO="$BASE_DIR/projects/$PROJECT_NAME"

# 색상 정의
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Git 저장소 초기화
echo -e "${BLUE}[INIT]${NC} Git 저장소 생성..."
mkdir -p $GIT_REPO
cd $GIT_REPO

if [ ! -d ".git" ]; then
    git init
    echo "# SmartPlug Pro - IoT Device Project" > README.md
    git add README.md
    git commit -m "Initial commit: SmartPlug Pro project"
    echo -e "${GREEN}✓${NC} Git 저장소가 생성되었습니다."
else
    echo -e "${YELLOW}!${NC} Git 저장소가 이미 존재합니다."
fi

# 기본 브랜치 생성
echo -e "\n${BLUE}[BRANCHES]${NC} 기본 브랜치 생성..."
git checkout -b main 2>/dev/null || git checkout main
git checkout -b develop 2>/dev/null || git checkout develop

# 각 에이전트별 Worktree 생성
echo -e "\n${BLUE}[WORKTREE]${NC} 에이전트별 작업 공간 생성..."

# PM Worktree
WORKTREE_PM="$BASE_DIR/projects/worktree-pm"
if [ ! -d "$WORKTREE_PM" ]; then
    git worktree add -b feature/product-spec "$WORKTREE_PM" develop
    echo -e "${GREEN}✓${NC} PM Claude 작업공간: $WORKTREE_PM"
    
    # PM 초기 파일 생성
    cat > "$WORKTREE_PM/product-spec.md" << 'EOF'
# SmartPlug Pro - Product Specification

## Product Overview
- **Name**: SmartPlug Pro
- **Category**: Smart Home / Energy Management
- **Target Market**: Korean households

## Core Features
1. Remote ON/OFF control
2. Real-time power monitoring
3. Schedule automation
4. Energy usage analytics
5. Overcurrent protection

## Technical Requirements
- MCU: ESP32-C3
- Power Measurement: HLW8032
- Connectivity: WiFi 2.4GHz, BLE 5.0
- Max Load: 16A / 3520W
- Input: AC 220V 50/60Hz
EOF
    cd "$WORKTREE_PM"
    git add .
    git commit -m "PM: Initial product specification"
fi

# Hardware Worktree
WORKTREE_HW="$BASE_DIR/projects/worktree-hardware"
if [ ! -d "$WORKTREE_HW" ]; then
    git worktree add -b feature/hardware "$WORKTREE_HW" develop
    echo -e "${GREEN}✓${NC} Hardware Claude 작업공간: $WORKTREE_HW"
    
    # Hardware 디렉토리 구조
    mkdir -p "$WORKTREE_HW"/{pcb,firmware,mechanical}
    
    # 기본 펌웨어 구조
    cat > "$WORKTREE_HW/firmware/main.c" << 'EOF'
/**
 * SmartPlug Pro Firmware
 * Platform: ESP32-C3
 */

#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "esp_wifi.h"

void app_main(void) {
    printf("SmartPlug Pro v1.0.0\n");
    // Initialize hardware
    // Setup WiFi
    // Start MQTT client
    // Main loop
}
EOF
    cd "$WORKTREE_HW"
    git add .
    git commit -m "Hardware: Initial firmware structure"
fi

# Backend Worktree
WORKTREE_BE="$BASE_DIR/projects/worktree-backend"
if [ ! -d "$WORKTREE_BE" ]; then
    git worktree add -b feature/backend "$WORKTREE_BE" develop
    echo -e "${GREEN}✓${NC} Backend Claude 작업공간: $WORKTREE_BE"
    
    # Backend 구조
    mkdir -p "$WORKTREE_BE"/{src,tests,config}
    
    # package.json
    cat > "$WORKTREE_BE/package.json" << 'EOF'
{
  "name": "smartplug-pro-backend",
  "version": "1.0.0",
  "description": "SmartPlug Pro API Server",
  "main": "src/index.js",
  "scripts": {
    "start": "node src/index.js",
    "dev": "nodemon src/index.js",
    "test": "jest"
  },
  "dependencies": {
    "express": "^4.18.0",
    "mqtt": "^5.0.0",
    "pg": "^8.11.0",
    "redis": "^4.6.0"
  }
}
EOF
    cd "$WORKTREE_BE"
    git add .
    git commit -m "Backend: Initial server setup"
fi

# Frontend Worktree
WORKTREE_FE="$BASE_DIR/projects/worktree-frontend"
if [ ! -d "$WORKTREE_FE" ]; then
    git worktree add -b feature/frontend "$WORKTREE_FE" develop
    echo -e "${GREEN}✓${NC} Frontend Claude 작업공간: $WORKTREE_FE"
    
    # Frontend 구조
    mkdir -p "$WORKTREE_FE"/{web,mobile}
    
    # React 앱 설정
    cat > "$WORKTREE_FE/web/package.json" << 'EOF'
{
  "name": "smartplug-pro-web",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "typescript": "^5.0.0",
    "tailwindcss": "^3.3.0",
    "recharts": "^2.5.0"
  }
}
EOF
    cd "$WORKTREE_FE"
    git add .
    git commit -m "Frontend: Initial React setup"
fi

# QA Worktree
WORKTREE_QA="$BASE_DIR/projects/worktree-qa"
if [ ! -d "$WORKTREE_QA" ]; then
    git worktree add -b feature/testing "$WORKTREE_QA" develop
    echo -e "${GREEN}✓${NC} QA Claude 작업공간: $WORKTREE_QA"
    
    # QA 구조
    mkdir -p "$WORKTREE_QA"/{unit-tests,integration-tests,e2e-tests,docs}
    
    # 테스트 계획
    cat > "$WORKTREE_QA/test-plan.md" << 'EOF'
# SmartPlug Pro - Test Plan

## Test Coverage
1. Hardware Tests
   - Power measurement accuracy
   - WiFi connectivity stability
   - Relay switching reliability
   
2. Backend Tests
   - API endpoint validation
   - Database integrity
   - MQTT message handling
   
3. Frontend Tests
   - UI component testing
   - User flow validation
   - Cross-browser compatibility

## Automation
- GitHub Actions CI/CD
- Jest for unit tests
- Cypress for E2E tests
EOF
    cd "$WORKTREE_QA"
    git add .
    git commit -m "QA: Initial test plan"
fi

# Worktree 상태 확인
echo -e "\n${BLUE}[STATUS]${NC} Git Worktree 상태:"
cd $GIT_REPO
git worktree list

# 각 에이전트에게 작업 공간 할당
echo -e "\n${BLUE}[ASSIGN]${NC} 에이전트별 작업 공간 매핑..."

# 심볼릭 링크 생성
ln -sf "$WORKTREE_PM" "$BASE_DIR/pm-workspace/project" 2>/dev/null
ln -sf "$WORKTREE_HW" "$BASE_DIR/engineering/hardware/project" 2>/dev/null
ln -sf "$WORKTREE_BE" "$BASE_DIR/engineering/backend/project" 2>/dev/null
ln -sf "$WORKTREE_FE" "$BASE_DIR/engineering/frontend/project" 2>/dev/null
ln -sf "$WORKTREE_QA" "$BASE_DIR/qa/project" 2>/dev/null

echo -e "${GREEN}✓${NC} 심볼릭 링크가 생성되었습니다."

# 협업 가이드
echo -e "\n${YELLOW}═══════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}           Git Worktree 협업 가이드${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════${NC}"
echo ""
echo "각 에이전트는 독립된 브랜치에서 작업합니다:"
echo "  • PM Claude:       feature/product-spec"
echo "  • Hardware Claude: feature/hardware"
echo "  • Backend Claude:  feature/backend"
echo "  • Frontend Claude: feature/frontend"
echo "  • QA Claude:       feature/testing"
echo ""
echo "병합 프로세스:"
echo "  1. 각 에이전트가 작업 완료 후 commit"
echo "  2. develop 브랜치로 Pull Request"
echo "  3. QA Claude가 테스트 실행"
echo "  4. CEO 승인 후 main 브랜치로 병합"
echo ""
echo "명령어:"
echo "  • 상태 확인: git worktree list"
echo "  • 브랜치 전환: cd /path/to/worktree"
echo "  • 동기화: git pull origin develop"
echo ""
echo -e "${GREEN}✅ Git Worktree 설정이 완료되었습니다!${NC}"