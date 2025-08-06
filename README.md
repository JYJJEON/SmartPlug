# 🚀 SmartPlug Pro - AI Team Collaboration Project

## 🏢 Project Overview
**Project Name**: SmartPlug Pro  
**Type**: IoT Smart Home Device Simulation  
**Purpose**: Demonstrating AI agent collaboration for product development  
**Status**: Proof of Concept / Learning Project

## 👥 Team Structure (Simulated AI Agents)

This project simulates a startup team using 5 AI agents working together:

### 1. PM Agent (Product Manager)
- Handles product planning and specifications
- Creates product proposals
- Manages development roadmap
- Coordinates between other agents

### 2. Hardware Agent (Hardware Engineer)
- Designs PCB layouts (simulated)
- Creates firmware specifications
- Plans hardware architecture
- Manages component selection

### 3. Backend Agent (Backend Developer)
- Develops API structure
- Database schema design
- IoT communication protocols
- Server architecture planning

### 4. Frontend Agent (UI/UX Developer)
- Web dashboard design
- Mobile app interface
- User experience optimization
- Data visualization components

### 5. QA Agent (Quality Assurance)
- Test planning
- Bug tracking simulation
- Performance monitoring
- Documentation management

## 🎯 How It Works

This is an experimental project that demonstrates how multiple AI agents can collaborate on a product development workflow:

1. **CEO (Human)** assigns tasks through the dashboard
2. **AI Agents** pick up tasks from the shared workspace
3. Each agent processes tasks based on their role
4. Agents communicate through a message system
5. Results are stored in the shared workspace

## 🛠️ Technical Implementation

### System Components
```
/claudeteam-startup/
├── agents/              # AI agent simulators
│   ├── agent_simulator.py
│   └── *_claude.sh     # Agent launch scripts
├── ceo-dashboard.py    # Management interface
├── shared-workspace/   # Inter-agent communication
│   ├── tasks/         # Task queue system
│   ├── messages/      # Agent messaging
│   └── status/        # Real-time status
└── startup_sim.sh     # System launcher
```

### Technologies Used
- **Python**: Agent simulation logic
- **Bash**: System orchestration
- **JSON**: Data storage and messaging
- **tmux**: Process management

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- tmux (for session management)
- Git

### Installation & Running

```bash
# Clone the repository
git clone https://github.com/JYJJEON/SmartPlug.git
cd SmartPlug

# Make scripts executable
chmod +x startup_sim.sh

# Start the simulation
./startup_sim.sh

# Check agent status
python3 ceo-dashboard.py status

# Assign tasks to agents
python3 ceo-dashboard.py assign pm_claude "Create product specification"

# View agent sessions
tmux ls
tmux attach -t pm_claude
```

## 📊 Features Demonstrated

### Task Management System
- Automated task distribution
- Priority-based task processing
- Task status tracking (pending → in_progress → completed)

### Inter-Agent Communication
- Message passing between agents
- Shared workspace for collaboration
- Status updates and reporting

### CEO Dashboard
- Real-time team status monitoring
- Task assignment interface
- Proposal review system
- Report generation

## 🎮 Usage Examples

```bash
# Assign a task to PM agent
python3 ceo-dashboard.py assign pm_claude "Research competitor products"

# Send message to an agent
python3 ceo-dashboard.py message backend_claude "Please prioritize API development"

# Review product proposals
python3 ceo-dashboard.py proposals

# Emergency meeting
python3 ceo-dashboard.py meeting "Urgent: Architecture review needed"
```

## 📝 Learning Objectives

This project demonstrates:
- Multi-agent system design
- Task queue implementation
- Inter-process communication
- Autonomous agent behavior simulation
- Collaborative workflow automation

## ⚠️ Limitations

- This is a **simulation/proof of concept**, not a production system
- Agents use simplified logic, not actual AI models
- No real hardware or IoT devices involved
- Designed for learning and experimentation

## 🔄 Current Status

- ✅ Basic agent framework implemented
- ✅ Task management system working
- ✅ Inter-agent communication established
- ✅ CEO dashboard functional
- 🔄 Improving agent intelligence
- 📋 Planning integration with real AI APIs

## 🤝 Contributing

This is an experimental learning project. Feel free to:
- Fork and experiment with your own agent behaviors
- Suggest improvements to the collaboration system
- Add new agent types or capabilities

## 📧 Contact

**Developer**: JYJJEON  
**Email**: james9434@gmail.com  
**GitHub**: https://github.com/JYJJEON/SmartPlug

## 📄 License

This project is for educational purposes. Feel free to use and modify for learning.

---

**Note**: This is a simulation project for demonstrating AI agent collaboration concepts. The "agents" are Python scripts simulating autonomous behavior, not actual AI team members.