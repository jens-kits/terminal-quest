# TerminalQuest/games/alignment_quest/custom_logic.py

import random

class GameLogic:
    def __init__(self, game):
        self.game = game
        self.alignment_score = 0
        self.innovation_score = 0
        self.efficiency_score = 0
        self.team_morale = 100
        self.max_alignment = 100
        self.used_items = set()
        self.visited_locations = set()
        self.completed_actions = set()
        self.sprint_number = 1
        self.backlog_health = 50

    def check_game_over(self):
        if self.alignment_score >= self.max_alignment:
            return True
        if self.team_morale <= 0:
            return True
        return False

    def handle_menu_choice(self, choice):
        if not self.game.active_menu:
            return "There is no active menu."
        
        try:
            choice = int(choice)
        except ValueError:
            return "Please enter a number to make your choice."
        
        if 1 <= choice <= len(self.game.active_menu):
            selected_option = self.game.active_menu[choice - 1]
            if 'action' in selected_option:
                action = selected_option['action']
                return self.execute_action(action)
            result = selected_option.get('result', "Nothing happens.")
            if selected_option.get('clear_menu', False):
                self.game.active_menu = None
            return result
        elif choice == len(self.game.active_menu) + 1:  # Option to exit menu
            self.game.active_menu = None
            return "You step away from the object."
        else:
            return "Invalid choice. Please try again."

    def display_menu(self, active_menu):
        menu_text = "What would you like to do?\n"
        for i, option in enumerate(active_menu, 1):
            menu_text += f"{i}. {option['name']}\n"
        menu_text += f"{len(active_menu) + 1}. Step away from the object"
        return menu_text

    def use_item(self, item_name):
        if item_name in self.used_items:
            return f"You've already used the {item_name}. Its effects are still active."
        
        self.used_items.add(item_name)
        
        if item_name == "golden sticky note":
            self.alignment_score += 10
            return "You use the Golden Sticky Note to prioritize a critical user story. The team rallies around this clear direction, improving overall alignment."
        elif item_name == "sprint planning toolkit":
            self.efficiency_score += 15
            return "You facilitate an effective sprint planning session using the toolkit. The team emerges with a clear, achievable sprint goal."
        elif item_name == "future scope glasses":
            self.innovation_score += 20
            return "Wearing the Future Scope Glasses, you gain valuable insights into potential product directions. This helps in making informed long-term decisions."
        elif item_name == "framework tuning fork":
            self.alignment_score += 15
            return "You use the Framework Tuning Fork on the dependency web. The resonance highlights misalignments in the program, allowing you to make critical adjustments."
        elif item_name == "burnout shield":
            self.team_morale += 20
            return "You deploy the Burnout Shield, providing temporary relief to an overwhelmed team. Their morale improves significantly."
        elif item_name == "collaboration catalyst":
            self.alignment_score += 10
            self.team_morale += 10
            return "You use the Collaboration Catalyst, fostering better communication and teamwork across the program."
        elif item_name == "devops harmony flute":
            self.efficiency_score += 20
            return "You play the DevOps Harmony Flute, aligning the rhythms of development and operations. The CI/CD pipeline flows more smoothly."
        elif item_name == "customer insight gem":
            self.innovation_score += 15
            self.alignment_score += 5
            return "You examine the Customer Insight Gem, gaining deep understanding of user needs. This insight helps align the team's efforts with customer value."
        elif item_name == "release conductor baton":
            self.efficiency_score += 15
            self.alignment_score += 10
            return "You wave the Release Conductor Baton, orchestrating a smooth and synchronized release process across teams."
        elif item_name == "dependency scissors":
            self.alignment_score += 10
            self.efficiency_score += 5
            return "You use the Dependency Scissors to cut through some tangled dependencies, simplifying the project structure."
        elif item_name == "feature polish cloth":
            self.innovation_score += 10
            self.alignment_score += 5
            return "You polish a key feature, enhancing its clarity and value proposition. The team's enthusiasm for the feature increases."
        elif item_name == "backlog pruning shears":
            self.backlog_health += 20
            return "You carefully prune the backlog, removing outdated or low-value items. The remaining backlog is more focused and manageable."
        elif item_name == "flow accelerator":
            self.efficiency_score += 20
            return "You apply the Flow Accelerator to a major bottleneck, significantly improving the speed of value delivery."
        elif item_name == "rejuvenation elixir":
            self.team_morale += 30
            return "You distribute the Rejuvenation Elixir to the team. Their energy and motivation are restored, preventing potential burnout."
        elif item_name == "automation wand":
            self.efficiency_score += 25
            return "You wave the Automation Wand, transforming a time-consuming manual process into an efficient automated one."
        else:
            return f"You can't use the {item_name} here."

    def execute_action(self, action):
        if action == "conduct_sprint_review":
            return self.conduct_sprint_review()
        elif action == "resolve_dependency":
            return self.resolve_dependency()
        elif action == "innovate_feature":
            return self.innovate_feature()
        elif action == "improve_ci_cd":
            return self.improve_ci_cd()
        elif action == "analyze_customer_feedback":
            return self.analyze_customer_feedback()
        elif action == "refine_backlog":
            return self.refine_backlog()
        else:
            return f"Unknown action: {action}"

    def conduct_sprint_review(self):
        self.sprint_number += 1
        alignment_boost = random.randint(5, 15)
        self.alignment_score += alignment_boost
        self.completed_actions.add("sprint_review")
        return f"You conduct a sprint review. The team's progress is evident, and stakeholders are pleased. Alignment improves by {alignment_boost} points."

    def resolve_dependency(self):
        if "resolve_dependency" in self.completed_actions:
            return "You've already resolved major dependencies in this PI."
        self.alignment_score += 15
        self.efficiency_score += 10
        self.completed_actions.add("resolve_dependency")
        return "You successfully resolve a critical dependency between teams. This improves both alignment and efficiency."

    def innovate_feature(self):
        if self.innovation_score < 30:
            return "The team doesn't have enough innovative ideas to create a groundbreaking feature yet."
        self.innovation_score -= 30
        self.alignment_score += 20
        return "Drawing on accumulated innovative ideas, the team creates a groundbreaking new feature that aligns perfectly with customer needs."

    def improve_ci_cd(self):
        if "improve_ci_cd" in self.completed_actions:
            return "You've already made significant improvements to the CI/CD pipeline in this PI."
        self.efficiency_score += 25
        self.completed_actions.add("improve_ci_cd")
        return "You lead an initiative to improve the CI/CD pipeline. Deployment frequency increases and lead time decreases significantly."

    def analyze_customer_feedback(self):
        self.innovation_score += 15
        self.alignment_score += 10
        return "You spend time analyzing recent customer feedback. This provides valuable insights that help align the team's efforts with customer needs."

    def refine_backlog(self):
        if self.backlog_health >= 80:
            return "The backlog is already in good shape and doesn't need refinement right now."
        self.backlog_health += 15
        self.alignment_score += 5
        return "You lead a backlog refinement session. The backlog is now more organized and better aligned with program goals."

    def get_game_status(self):
        status = f"Alignment Score: {self.alignment_score}\n"
        status += f"Innovation Score: {self.innovation_score}\n"
        status += f"Efficiency Score: {self.efficiency_score}\n"
        status += f"Team Morale: {self.team_morale}\n"
        status += f"Sprint Number: {self.sprint_number}\n"
        status += f"Backlog Health: {self.backlog_health}\n"
        return status

    def get_alignment_status(self):
        if self.alignment_score < 30:
            return "The teams are struggling to align. There's a lot of confusion and miscommunication."
        elif self.alignment_score < 60:
            return "There's progress in alignment, but some teams are still out of sync."
        elif self.alignment_score < 90:
            return "The alignment is good! Most teams are working well together, with only minor discrepancies."
        else:
            return "Excellent alignment! The teams are working in perfect harmony towards common goals."

    def end_turn(self):
        self.team_morale -= 5  # Natural decrease in morale over time
        if self.backlog_health > 0:
            self.backlog_health -= 2  # Backlog naturally becomes less healthy over time
        
        # Random events
        if random.random() < 0.1:  # 10% chance of random event
            event = random.choice(["production_issue", "market_change", "team_conflict"])
            if event == "production_issue":
                self.efficiency_score -= 10
                return "A production issue has been discovered, decreasing overall efficiency."
            elif event == "market_change":
                self.innovation_score -= 10
                return "A sudden market change has made some of your innovative ideas less relevant."
            elif event == "team_conflict":
                self.team_morale -= 15
                return "A conflict has arisen between team members, decreasing overall morale."

        return "The day ends. The team rests and prepares for tomorrow's challenges."

    def custom_command_handler(self, command):
        if command == "status":
            return self.get_game_status()
        elif command == "alignment":
            return self.get_alignment_status()
        return None

    def show_credits(self):
        return """
ALIGNMENT QUEST: THE SCALED AGILE SAGA
A SAFe Adventure in Agile Wonderland

Created by:
- Your Name
- TerminalQuest Team

Special thanks to all Agile practitioners who inspire us to continually improve!

Thank you for playing!
        """