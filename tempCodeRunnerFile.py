class SeatingArrangement:
    def __init__(self, people, constraints):
        self.people = people
        self.n = len(people)
        self.constraints = constraints
        self.arrangement = [-1] * self.n
        self.used = [False] * self.n
    
    def is_valid(self, position, person_idx):
        """Check if placing person at position satisfies constraints"""
        # Check must_sit_together constraints
        if 'must_sit_together' in self.constraints:
            for pair in self.constraints['must_sit_together']:
                p1_idx = self.people.index(pair[0])
                p2_idx = self.people.index(pair[1])
                
                # If one is placed, check if other can be adjacent
                if person_idx == p1_idx:
                    if p2_idx in self.arrangement[:position]:
                        pos = self.arrangement.index(p2_idx)
                        if abs(pos - position) != 1:
                            return False
                elif person_idx == p2_idx:
                    if p1_idx in self.arrangement[:position]:
                        pos = self.arrangement.index(p1_idx)
                        if abs(pos - position) != 1:
                            return False
        
        # Check cannot_sit_together constraints
        if 'cannot_sit_together' in self.constraints:
            for pair in self.constraints['cannot_sit_together']:
                p1_idx = self.people.index(pair[0])
                p2_idx = self.people.index(pair[1])
                
                if person_idx == p1_idx and p2_idx in self.arrangement[:position]:
                    pos = self.arrangement.index(p2_idx)
                    if abs(pos - position) == 1:
                        return False
                elif person_idx == p2_idx and p1_idx in self.arrangement[:position]:
                    pos = self.arrangement.index(p1_idx)
                    if abs(pos - position) == 1:
                        return False
        
        return True
    
    def solve(self, position=0):
        """Backtracking function to arrange seating"""
        # Base case: all positions filled
        if position == self.n:
            return True
        
        # Try each person in current position
        for person_idx in range(self.n):
            if not self.used[person_idx] and self.is_valid(position, person_idx):
                # Assign person to position
                self.arrangement[position] = person_idx
                self.used[person_idx] = True
                
                # Recursively fill remaining positions
                if self.solve(position + 1):
                    return True
                
                # Backtrack
                self.arrangement[position] = -1
                self.used[person_idx] = False
        
        return False
    
    def get_solution(self):
        if self.solve():
            return [self.people[i] for i in self.arrangement]
        return None


# Example: Seating arrangement with constraints
def seating_arrangement_example():
    people = ["Alice", "Bob", "Charlie", "Diana", "Eve"]
    
    constraints = {
        'must_sit_together': [("Alice", "Bob")],
        'cannot_sit_together': [("Charlie", "Diana")]
    }
    
    sa = SeatingArrangement(people, constraints)
    solution = sa.get_solution()
    
    print("\n\nSeating Arrangement Solution:")
    print("-" * 40)
    print("Constraints:")
    print("- Alice and Bob must sit together")
    print("- Charlie and Diana cannot sit together\n")
    
    if solution:
        print("Seating Order:")
        for i, person in enumerate(solution):
            print(f"Seat {i+1}: {person}")
        return True
    else:
        print("No valid arrangement found")
        return False


# Run both examples
if __name__ == "__main__":
    seating_arrangement_example()