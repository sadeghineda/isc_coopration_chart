import sqlite3
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

class OrgChart:
    def __init__(self, db_path):
        """Initialize with database connection"""
        self.db_path = db_path
        self.conn = None
        self.employees = {}
        self.hierarchy = defaultdict(list)
        
    def connect_db(self):
        """Connect to the database"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        
    def fetch_data(self):
        """Fetch employee data from database"""
        cursor = self.conn.cursor()
        
        # Adjust this query based on your actual table structure
        query = """
        SELECT employee_id, name, position, manager_id, department
        FROM employees
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        for row in rows:
            emp_id = row['employee_id']
            self.employees[emp_id] = {
                'id': emp_id,
                'name': row['name'],
                'position': row['position'],
                'manager_id': row['manager_id'],
                'department': row['department']
            }
            
            # Build hierarchy
            manager_id = row['manager_id']
            if manager_id:
                self.hierarchy[manager_id].append(emp_id)
            
    def get_root_employees(self):
        """Find employees with no manager (top of hierarchy)"""
        return [emp_id for emp_id, emp in self.employees.items() 
                if emp['manager_id'] is None]
    
    def print_hierarchy(self, emp_id=None, level=0):
        """Print text-based hierarchy"""
        if emp_id is None:
            roots = self.get_root_employees()
            for root in roots:
                self.print_hierarchy(root, 0)
            return
            
        emp = self.employees[emp_id]
        indent = "  " * level
        print(f"{indent}├─ {emp['name']} - {emp['position']} ({emp['department']})")
        
        for subordinate_id in self.hierarchy[emp_id]:
            self.print_hierarchy(subordinate_id, level + 1)
    
    def visualize_chart(self):
        """Create visual org chart using matplotlib"""
        fig, ax = plt.subplots(figsize=(14, 10))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Position tracking
        positions = {}
        
        def calculate_positions(emp_id, x, y, width):
            """Recursively calculate positions for employees"""
            positions[emp_id] = (x, y)
            
            subordinates = self.hierarchy[emp_id]
            if subordinates:
                sub_width = width / len(subordinates)
                start_x = x - width/2 + sub_width/2
                
                for i, sub_id in enumerate(subordinates):
                    sub_x = start_x + i * sub_width
                    calculate_positions(sub_id, sub_x, y - 1.5, sub_width * 0.8)
        
        # Calculate positions starting from root
        roots = self.get_root_employees()
        for i, root in enumerate(roots):
            calculate_positions(root, 5 + i * 2, 9, 8)
        
        # Draw connections and boxes
        for emp_id, (x, y) in positions.items():
            emp = self.employees[emp_id]
            
            # Draw connections to subordinates
            for sub_id in self.hierarchy[emp_id]:
                if sub_id in positions:
                    sub_x, sub_y = positions[sub_id]
                    ax.plot([x, sub_x], [y - 0.3, sub_y + 0.3], 
                           'k-', linewidth=1.5, alpha=0.6)
            
            # Draw employee box
            box = FancyBboxPatch((x - 0.6, y - 0.25), 1.2, 0.5,
                                boxstyle="round,pad=0.05", 
                                edgecolor='#2C3E50', 
                                facecolor='#3498DB',
                                linewidth=2)
            ax.add_patch(box)
            
            # Add text
            ax.text(x, y + 0.1, emp['name'], 
                   ha='center', va='center', 
                   fontsize=9, fontweight='bold', color='white')
            ax.text(x, y - 0.1, emp['position'], 
                   ha='center', va='center', 
                   fontsize=7, color='white', style='italic')
        
        plt.title('Organization Chart', fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig('org_chart.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


# Example usage
if __name__ == "__main__":
    # Create sample database for demonstration
    def create_sample_db():
        conn = sqlite3.connect('company.db')
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            employee_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            position TEXT NOT NULL,
            manager_id INTEGER,
            department TEXT,
            FOREIGN KEY (manager_id) REFERENCES employees (employee_id)
        )
        ''')
        
        # Sample data
        employees = [
            (1, 'John Smith', 'CEO', None, 'Executive'),
            (2, 'Sarah Johnson', 'CTO', 1, 'Technology'),
            (3, 'Mike Brown', 'CFO', 1, 'Finance'),
            (4, 'Emily Davis', 'VP Engineering', 2, 'Technology'),
            (5, 'David Wilson', 'VP Product', 2, 'Technology'),
            (6, 'Lisa Anderson', 'Senior Developer', 4, 'Technology'),
            (7, 'Tom Martinez', 'Senior Developer', 4, 'Technology'),
            (8, 'Anna Taylor', 'Product Manager', 5, 'Technology'),
            (9, 'James Lee', 'Accountant', 3, 'Finance'),
        ]
        
        cursor.execute('DELETE FROM employees')
        cursor.executemany('INSERT INTO employees VALUES (?,?,?,?,?)', employees)
        conn.commit()
        conn.close()
    
    # Create sample database
    create_sample_db()
    
    # Generate org chart
    org = OrgChart('company.db')
    org.connect_db()
    org.fetch_data()
    
    print("=== Organization Hierarchy ===\n")
    org.print_hierarchy()
    
    print("\n=== Generating Visual Chart ===")
    org.visualize_chart()
    
    org.close()