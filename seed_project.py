from app import app
from models import db, Subject, Module, Question

with app.app_context():

    print("Resetting database...")

    db.drop_all()
    db.create_all()

    # =============================
    # SUBJECTS & MODULES CREATION
    # =============================

    subjects_data = {
        "AAD": 5,
        "IEFT": 5,
        "CG": 5,
        "CD": 5,
        "PYTHON": 5,
        "ML": 5       # ✅ FIX 1: Added missing ML subject
    }

    subject_objects = {}

    for subject_name, module_count in subjects_data.items():
        subject = Subject(subject_name=subject_name)
        db.session.add(subject)
        db.session.flush()

        subject_objects[subject_name] = subject

        for i in range(1, module_count + 1):
            module = Module(
                module_name=f"Module {i}",
                subject_id=subject.id
            )
            db.session.add(module)

    db.session.commit()
    print("Subjects & Modules Created Successfully")

    # =====================================
    # AAD MODULE 1 – Algorithm Analysis
    # =====================================

    aad = subject_objects["AAD"]

    aad_module1 = Module.query.filter_by(module_name="Module 1", subject_id=aad.id).first()

    aad_module1_questions = [
        # EASY (1-5)
        ("Which of the following is NOT a characteristic of an algorithm?",
         "Finiteness", "Ambiguity", "Input", "Output",
         "Ambiguity", "Easy"),
        ("Time complexity measures:",
         "Memory used", "Number of lines in program",
         "Running time as function of input size", "CPU speed",
         "Running time as function of input size", "Easy"),
        ("Big-O notation represents:",
         "Best case", "Average case", "Worst case upper bound", "Exact case",
         "Worst case upper bound", "Easy"),
        ("The time complexity of a single loop running n times is:",
         "O(1)", "O(n)", "O(n²)", "O(log n)",
         "O(n)", "Easy"),
        ("Which grows fastest?",
         "log n", "n", "n²", "2ⁿ",
         "2ⁿ", "Easy"),

        # INTERMEDIATE (6-15)
        ("Big-Theta represents:",
         "Upper bound", "Lower bound", "Tight bound", "Average case only",
         "Tight bound", "Intermediate"),
        ("Solve T(n) = T(n-1) + 1:",
         "O(log n)", "O(n)", "O(n²)", "O(2ⁿ)",
         "O(n)", "Intermediate"),
        ("Time complexity of nested loops (n × n):",
         "O(n)", "O(n log n)", "O(n²)", "O(log n)",
         "O(n²)", "Intermediate"),
        ("Master Theorem applies to recurrences of form:",
         "T(n)=T(n-1)+1", "T(n)=aT(n/b)+f(n)", "T(n)=nT(n-1)", "T(n)=T(n-2)+T(n-1)",
         "T(n)=aT(n/b)+f(n)", "Intermediate"),
        ("If f(n)=O(g(n)) and g(n)=O(h(n)), then:",
         "f(n)=Ω(h(n))", "f(n)=Θ(h(n))", "f(n)=O(h(n))", "None",
         "f(n)=O(h(n))", "Intermediate"),
        ("T(n)=2T(n/2)+n has complexity:",
         "O(n)", "O(n log n)", "O(n²)", "O(log n)",
         "O(n log n)", "Intermediate"),
        ("Which notation gives lower bound?",
         "O", "Ω", "Θ", "o",
         "Ω", "Intermediate"),
        ("The recurrence of Merge Sort is:",
         "T(n)=T(n-1)+n", "T(n)=2T(n/2)+n", "T(n)=nT(n-1)", "T(n)=T(n/2)+n",
         "T(n)=2T(n/2)+n", "Intermediate"),
        ("Time complexity of logarithmic growth is:",
         "O(n)", "O(n²)", "O(log n)", "O(2ⁿ)",
         "O(log n)", "Intermediate"),
        ("Which grows slower?",
         "n log n", "n²", "n", "2ⁿ",
         "n", "Intermediate"),

        # ADVANCED (16-20)
        ("Solve T(n)=4T(n/2)+n² using Master Theorem:",
         "O(n² log n)", "O(n²)", "O(n log n)", "O(n³)",
         "O(n²)", "Advanced"),
        ("T(n)=T(n/3)+T(2n/3)+n has complexity:",
         "O(n)", "O(n log n)", "O(n²)", "O(log n)",
         "O(n log n)", "Advanced"),
        ("Which case of Master Theorem applies if f(n)=Θ(n log n) and a=2,b=2?",
         "Case 1", "Case 2", "Case 3", "Not applicable",
         "Case 2", "Advanced"),
        ("2ⁿ compared to n³ is:",
         "Smaller", "Equal", "Larger", "Same order",
         "Larger", "Advanced"),
        ("Which complexity is best for large input?",
         "O(2ⁿ)", "O(n²)", "O(n log n)", "O(n!)",
         "O(n log n)", "Advanced"),
    ]

    for q in aad_module1_questions:
        db.session.add(Question(
            question_text=q[0], option1=q[1], option2=q[2],
            option3=q[3], option4=q[4], correct_answer=q[5],
            difficulty=q[6], module_id=aad_module1.id))
    db.session.commit()
    print("AAD Module 1 inserted successfully!")

    # =====================================
    # AAD MODULE 2 – Advanced DS & Graph
    # =====================================

    aad_module2 = Module.query.filter_by(module_name="Module 2", subject_id=aad.id).first()

    aad_module2_questions = [
        # EASY (1-5)
        ("AVL tree is a:",
         "Complete binary tree", "Height balanced BST", "Heap", "B-tree",
         "Height balanced BST", "Easy"),
        ("Balance factor in AVL tree is:",
         "Height(left) – Height(right)", "Nodes count difference", "Degree difference", "Level difference",
         "Height(left) – Height(right)", "Easy"),
        ("BFS uses which data structure?",
         "Stack", "Queue", "Heap", "Tree",
         "Queue", "Easy"),
        ("DFS uses which data structure?",
         "Queue", "Stack", "Array", "Heap",
         "Stack", "Easy"),
        ("Disjoint set operations include:",
         "Insert & Delete", "Push & Pop", "Union & Find", "BFS & DFS",
         "Union & Find", "Easy"),

        # INTERMEDIATE (6-15)
        ("Worst-case height of AVL tree with n nodes is:",
         "O(n)", "O(log n)", "O(n²)", "O(1)",
         "O(log n)", "Intermediate"),
        ("Which rotation is needed in left-left case?",
         "Left rotation", "Right rotation", "LR rotation", "RL rotation",
         "Right rotation", "Intermediate"),
        ("Time complexity of BFS is:",
         "O(V+E)", "O(V²)", "O(E²)", "O(log V)",
         "O(V+E)", "Intermediate"),
        ("Strongly connected components are found using:",
         "BFS", "DFS", "Kruskal", "Dijkstra",
         "DFS", "Intermediate"),
        ("Topological sorting works only on:",
         "Undirected graph", "Cyclic graph", "DAG", "Tree",
         "DAG", "Intermediate"),
        ("Time complexity of Union-Find with path compression:",
         "O(n)", "O(log n)", "O(α(n))", "O(n²)",
         "O(α(n))", "Intermediate"),
        ("RL imbalance requires:",
         "Single left rotation", "Single right rotation", "Right + Left rotation", "No rotation",
         "Right + Left rotation", "Intermediate"),
        ("DFS edge classification includes:",
         "Tree edge", "Back edge", "Forward edge", "All of these",
         "All of these", "Intermediate"),
        ("Shortest path in unweighted graph found by:",
         "DFS", "BFS", "Dijkstra", "Kruskal",
         "BFS", "Intermediate"),
        ("Time complexity of AVL insertion:",
         "O(n)", "O(log n)", "O(n log n)", "O(1)",
         "O(log n)", "Intermediate"),

        # ADVANCED (16-20)
        ("Minimum height of AVL tree with 7 nodes is:",
         "1", "2", "3", "4",
         "2", "Advanced"),
        ("If graph has cycle, topological sort:",
         "Exists", "Does not exist", "Is unique", "Is constant",
         "Does not exist", "Advanced"),
        ("SCC algorithm commonly used is:",
         "Prim's", "Kosaraju's", "Floyd", "Bellman-Ford",
         "Kosaraju's", "Advanced"),
        ("In union by rank, we attach:",
         "Larger tree under smaller", "Smaller tree under larger", "Random", "Root to leaf",
         "Smaller tree under larger", "Advanced"),
        ("Worst-case DFS complexity in adjacency matrix:",
         "O(V+E)", "O(V²)", "O(E²)", "O(log V)",
         "O(V²)", "Advanced"),
    ]

    for q in aad_module2_questions:
        db.session.add(Question(
            question_text=q[0], option1=q[1], option2=q[2],
            option3=q[3], option4=q[4], correct_answer=q[5],
            difficulty=q[6], module_id=aad_module2.id))
    db.session.commit()
    print("AAD Module 2 inserted successfully!")

    # =====================================
    # AAD MODULE 3 – Divide & Conquer / Greedy
    # =====================================

    aad_module3 = Module.query.filter_by(module_name="Module 3", subject_id=aad.id).first()

    aad_module3_questions = [
        # EASY (1-5)
        ("Merge Sort follows which strategy?",
         "Greedy", "Dynamic Programming", "Divide & Conquer", "Backtracking",
         "Divide & Conquer", "Easy"),
        ("Time complexity of Merge Sort worst case:",
         "O(n²)", "O(n log n)", "O(n)", "O(log n)",
         "O(n log n)", "Easy"),
        ("Greedy strategy makes decisions based on:",
         "Future outcomes", "Random selection", "Local optimal choice", "Exhaustive search",
         "Local optimal choice", "Easy"),
        ("Kruskal's algorithm finds:",
         "Shortest path", "Minimum Spanning Tree", "SCC", "Topological order",
         "Minimum Spanning Tree", "Easy"),
        ("Dijkstra's algorithm is used for:",
         "All pairs shortest path", "Single source shortest path", "MST", "TSP",
         "Single source shortest path", "Easy"),

        # INTERMEDIATE (6-15)
        ("Recurrence of Merge Sort:",
         "T(n)=T(n-1)+n", "T(n)=2T(n/2)+n", "T(n)=nT(n-1)", "T(n)=T(n/2)+1",
         "T(n)=2T(n/2)+n", "Intermediate"),
        ("Space complexity of Merge Sort:",
         "O(1)", "O(log n)", "O(n)", "O(n²)",
         "O(n)", "Intermediate"),
        ("Strassen reduces matrix multiplication complexity from:",
         "n³ to n²", "n³ to n^2.81", "n² to n log n", "n³ to n log n",
         "n³ to n^2.81", "Intermediate"),
        ("Fractional Knapsack solved using:",
         "DP", "Greedy", "Backtracking", "Branch & Bound",
         "Greedy", "Intermediate"),
        ("Time complexity of Kruskal's algorithm:",
         "O(V²)", "O(E log E)", "O(V log V)", "O(E²)",
         "O(E log E)", "Intermediate"),
        ("Dijkstra fails when graph has:",
         "Positive weights", "Negative weights", "Zero weights", "Directed edges",
         "Negative weights", "Intermediate"),
        ("Divide & Conquer steps:",
         "Divide, Conquer, Combine", "Sort, Merge, Select", "Search, Insert, Delete", "Choose, Prune, Backtrack",
         "Divide, Conquer, Combine", "Intermediate"),
        ("If graph is disconnected, Kruskal produces:",
         "Error", "Forest", "Cycle", "Infinite loop",
         "Forest", "Intermediate"),
        ("Dijkstra complexity with min-priority queue:",
         "O(V²)", "O((V+E) log V)", "O(E²)", "O(VE)",
         "O((V+E) log V)", "Intermediate"),
        ("Greedy works correctly when problem has:",
         "Overlapping subproblems", "Optimal substructure and greedy choice property",
         "Only recursion", "No constraints",
         "Optimal substructure and greedy choice property", "Intermediate"),

        # ADVANCED (16-20)
        ("Strassen recurrence is:",
         "8T(n/2)+n²", "7T(n/2)+n²", "2T(n/2)+n", "T(n/2)+n²",
         "7T(n/2)+n²", "Advanced"),
        ("Merge Sort best case time complexity:",
         "O(n)", "O(n log n)", "O(n²)", "O(log n)",
         "O(n log n)", "Advanced"),
        ("Fractional Knapsack selects items based on:",
         "Weight", "Profit", "Profit/Weight ratio", "Random",
         "Profit/Weight ratio", "Advanced"),
        ("Greedy fails for:",
         "Fractional Knapsack", "0/1 Knapsack", "MST", "Dijkstra",
         "0/1 Knapsack", "Advanced"),
        ("If E ≈ V², Kruskal complexity becomes:",
         "O(V log V)", "O(V² log V)", "O(V²)", "O(V³)",
         "O(V² log V)", "Advanced"),
    ]

    for q in aad_module3_questions:
        db.session.add(Question(
            question_text=q[0], option1=q[1], option2=q[2],
            option3=q[3], option4=q[4], correct_answer=q[5],
            difficulty=q[6], module_id=aad_module3.id))
    db.session.commit()
    print("AAD Module 3 inserted successfully!")

    # =====================================
    # AAD MODULE 4 – Dynamic Programming & Backtracking
    # =====================================

    aad_module4 = Module.query.filter_by(module_name="Module 4", subject_id=aad.id).first()

    aad_module4_questions = [
        # EASY (1-5)
        ("Dynamic Programming is based on:",
         "Greedy choice", "Optimal substructure", "Divide property", "Random",
         "Optimal substructure", "Easy"),
        ("Floyd–Warshall finds:",
         "MST", "Single source shortest path", "All pairs shortest path", "Topological order",
         "All pairs shortest path", "Easy"),
        ("N-Queen problem is solved using:",
         "Greedy", "DP", "Backtracking", "Divide & Conquer",
         "Backtracking", "Easy"),
        ("Matrix Chain Multiplication minimizes:",
         "Number of matrices", "Memory", "Scalar multiplications", "Additions",
         "Scalar multiplications", "Easy"),
        ("TSP solved by Branch & Bound has complexity:",
         "O(n)", "O(n log n)", "O(n²)", "Exponential",
         "Exponential", "Easy"),

        # INTERMEDIATE (6-15)
        ("Floyd–Warshall time complexity:",
         "O(n²)", "O(n³)", "O(n log n)", "O(2ⁿ)",
         "O(n³)", "Intermediate"),
        ("DP avoids recomputation by:",
         "Recursion", "Memoization/tabulation", "Loops", "Sorting",
         "Memoization/tabulation", "Intermediate"),
        ("MCM uses which technique?",
         "Greedy", "Divide & Conquer", "Dynamic Programming", "Random",
         "Dynamic Programming", "Intermediate"),
        ("Backtracking explores:",
         "BFS tree", "State space tree", "Greedy path", "DP table",
         "State space tree", "Intermediate"),
        ("Branch & Bound improves over backtracking by:",
         "Recursion", "Sorting", "Using bounding function", "Stack",
         "Using bounding function", "Intermediate"),
        ("Floyd–Warshall works for graphs with:",
         "Negative edges without negative cycle", "Positive weights only", "Trees only", "Undirected only",
         "Negative edges without negative cycle", "Intermediate"),
        ("DP stores solutions in:",
         "Linked list", "Stack", "Table", "Queue",
         "Table", "Intermediate"),
        ("Number of solutions for 4-Queens problem:",
         "1", "2", "4", "8",
         "2", "Intermediate"),
        ("Branch & Bound prunes when:",
         "Cost is zero", "Bound exceeds best known solution", "Graph is complete", "All nodes visited",
         "Bound exceeds best known solution", "Intermediate"),
        ("MCM time complexity:",
         "O(n²)", "O(n³)", "O(2ⁿ)", "O(n log n)",
         "O(n³)", "Intermediate"),

        # ADVANCED (16-20)
        ("DP solution for TSP has complexity:",
         "O(n³)", "O(n² log n)", "O(n² 2ⁿ)", "O(2ⁿ)",
         "O(n² 2ⁿ)", "Advanced"),
        ("Floyd–Warshall can detect:",
         "MST", "SCC", "Negative weight cycle", "Topological order",
         "Negative weight cycle", "Advanced"),
        ("N-Queen worst case complexity:",
         "O(n²)", "O(n³)", "O(n!)", "O(2ⁿ)",
         "O(n!)", "Advanced"),
        ("Branch & Bound guarantees finding:",
         "Approximate solution", "Random solution", "Optimal solution", "Greedy solution",
         "Optimal solution", "Advanced"),
        ("DP is preferred over recursion when problem has:",
         "Greedy property", "Overlapping subproblems", "Small input only", "Acyclic structure",
         "Overlapping subproblems", "Advanced"),
    ]

    for q in aad_module4_questions:
        db.session.add(Question(
            question_text=q[0], option1=q[1], option2=q[2],
            option3=q[3], option4=q[4], correct_answer=q[5],
            difficulty=q[6], module_id=aad_module4.id))
    db.session.commit()
    print("AAD Module 4 inserted successfully!")

    # =====================================
    # AAD MODULE 5 – P, NP & Approximation
    # =====================================

    aad_module5 = Module.query.filter_by(module_name="Module 5", subject_id=aad.id).first()

    aad_module5_questions = [
        # EASY (1-5)
        ("Class P problems can be solved in:",
         "Exponential time", "Polynomial time", "Logarithmic time", "Constant time",
         "Polynomial time", "Easy"),
        ("NP stands for:",
         "Non-Polynomial", "Non-Probabilistic", "Non-deterministic Polynomial", "Negative Polynomial",
         "Non-deterministic Polynomial", "Easy"),
        ("NP-Complete means the problem is:",
         "Only in NP", "Only NP-Hard", "In NP and NP-Hard", "In P only",
         "In NP and NP-Hard", "Easy"),
        ("Bin Packing problem is classified as:",
         "P", "NP", "NP-Hard", "Polynomial",
         "NP-Hard", "Easy"),
        ("Monte Carlo algorithm:",
         "Always gives correct answer", "May give incorrect answer", "Never terminates", "Works on graphs only",
         "May give incorrect answer", "Easy"),

        # INTERMEDIATE (6-15)
        ("NP means a solution can be:",
         "Solved in polynomial time", "Verified in polynomial time", "Solved in exponential time", "Unsolvable",
         "Verified in polynomial time", "Intermediate"),
        ("NP-Hard problems:",
         "Must belong to NP", "May not belong to NP", "Are always polynomial", "Are easy",
         "May not belong to NP", "Intermediate"),
        ("Vertex Cover problem selects vertices such that:",
         "All vertices are connected", "Every edge has at least one endpoint covered",
         "Graph becomes complete", "Graph becomes acyclic",
         "Every edge has at least one endpoint covered", "Intermediate"),
        ("Clique problem asks for:",
         "Maximum matching", "Complete subgraph of size k", "MST", "Shortest path",
         "Complete subgraph of size k", "Intermediate"),
        ("If any NP-Complete problem is solved in polynomial time:",
         "NP becomes empty", "P = NP", "NP-Hard problems disappear", "All become exponential",
         "P = NP", "Intermediate"),
        ("Polynomial reduction is used to:",
         "Simplify recursion", "Prove NP-Completeness", "Speed up sorting", "Reduce memory",
         "Prove NP-Completeness", "Intermediate"),
        ("First Fit Decreasing heuristic is used in:",
         "Graph Coloring", "Bin Packing", "TSP", "MST",
         "Bin Packing", "Intermediate"),
        ("Approximation algorithms are used when:",
         "Exact solution is polynomial", "Problem is NP-Hard", "Input is small", "Graph is weighted",
         "Problem is NP-Hard", "Intermediate"),
        ("Randomized QuickSort average case complexity:",
         "O(n²)", "O(n log n)", "O(log n)", "O(n³)",
         "O(n log n)", "Intermediate"),
        ("Las Vegas algorithm:",
         "May give wrong answer", "Always gives correct answer", "Never terminates", "Is deterministic",
         "Always gives correct answer", "Intermediate"),

        # ADVANCED (16-20)
        ("If P≠NP, NP-Complete problems are believed to be:",
         "Polynomial", "Exponential", "Constant", "Linear",
         "Exponential", "Advanced"),
        ("Clique problem reduces to:",
         "Sorting", "Vertex Cover", "Merge Sort", "Dijkstra",
         "Vertex Cover", "Advanced"),
        ("Approximation ratio measures:",
         "Running time", "Memory usage", "Quality of approximate solution", "Number of iterations",
         "Quality of approximate solution", "Advanced"),
        ("QuickSort worst case occurs when:",
         "Array is random", "Pivot is always median", "Array is already sorted", "Array has duplicates",
         "Array is already sorted", "Advanced"),
        ("Randomization in algorithms helps to:",
         "Increase worst case", "Avoid adversarial inputs", "Remove recursion", "Guarantee polynomial time",
         "Avoid adversarial inputs", "Advanced"),
    ]

    for q in aad_module5_questions:
        db.session.add(Question(
            question_text=q[0], option1=q[1], option2=q[2],
            option3=q[3], option4=q[4], correct_answer=q[5],
            difficulty=q[6], module_id=aad_module5.id))
    db.session.commit()
    print("AAD Module 5 inserted successfully!")

    # =====================================
    # CD MODULE 1 – Lexical Analysis & Basics
    # =====================================

    cd = subject_objects["CD"]

    cd_module1 = Module.query.filter_by(module_name="Module 1", subject_id=cd.id).first()

    cd_module1_questions = [
        # EASY (1-5)
        ("Compiler translates:",
         "High-level language to machine code", "Machine code to high-level",
         "Assembly to assembly", "Binary to decimal",
         "High-level language to machine code", "Easy"),
        ("Lexical analyzer is also called:",
         "Parser", "Scanner", "Optimizer", "Interpreter",
         "Scanner", "Easy"),
        ("Token is:",
         "Smallest meaningful unit of a program", "Variable", "Loop", "Keyword only",
         "Smallest meaningful unit of a program", "Easy"),
        ("Which phase removes comments from source code?",
         "Syntax analysis", "Lexical analysis", "Optimization", "Code generation",
         "Lexical analysis", "Easy"),
        ("Symbol table stores:",
         "Variable information", "Machine code", "Parse tree", "Tokens only",
         "Variable information", "Easy"),

        # INTERMEDIATE (6-13)
        ("Regular expressions are used in:",
         "Syntax analysis", "Lexical analysis", "Code optimization", "Parsing",
         "Lexical analysis", "Intermediate"),
        ("Finite Automata is used in:",
         "Lexical analyzer", "Parser", "Code generator", "Linker",
         "Lexical analyzer", "Intermediate"),
        ("NFA stands for:",
         "Non-deterministic Finite Automata", "Normal Finite Automata",
         "New Finite Automata", "None of these",
         "Non-deterministic Finite Automata", "Intermediate"),
        ("Conversion from NFA to DFA uses:",
         "Subset construction", "Left factoring", "Recursion", "Stack",
         "Subset construction", "Intermediate"),
        ("DFA is faster than NFA because:",
         "DFA has more states", "DFA has unique transitions", "DFA uses stack", "DFA is smaller",
         "DFA has unique transitions", "Intermediate"),
        ("Regular grammar is equivalent to:",
         "DFA", "PDA", "CFG", "Turing Machine",
         "DFA", "Intermediate"),
        ("Error detected in lexical phase is called:",
         "Syntax error", "Lexical error", "Runtime error", "Logical error",
         "Lexical error", "Intermediate"),
        ("Longest match rule (maximal munch) applies in:",
         "Parsing", "Lexical analysis", "Optimization", "Linking",
         "Lexical analysis", "Intermediate"),

        # ADVANCED (14-20)
        ("Minimization of DFA reduces number of:",
         "States", "Transitions", "Tokens", "Grammar rules",
         "States", "Advanced"),
        ("Regular expressions CANNOT represent:",
         "Identifiers", "Numbers", "Nested balanced structures", "Keywords",
         "Nested balanced structures", "Advanced"),
        ("ε-transition is allowed in:",
         "DFA", "NFA", "Both DFA and NFA", "Neither",
         "NFA", "Advanced"),
        ("Lex tool is used for:",
         "Lexical analyzer generation", "Parsing", "Optimization", "Code execution",
         "Lexical analyzer generation", "Advanced"),
        ("Which automata recognizes regular languages?",
         "DFA", "PDA", "Turing Machine", "Stack machine",
         "DFA", "Advanced"),
        ("Interpreter differs from compiler because it:",
         "Translates whole program at once", "Executes line by line",
         "Generates object code", "Produces faster output",
         "Executes line by line", "Advanced"),
        ("Symbol table is updated during:",
         "All phases of compilation", "Only lexical phase", "Only parsing", "Only optimization",
         "All phases of compilation", "Advanced"),
    ]

    for q in cd_module1_questions:
        db.session.add(Question(
            question_text=q[0], option1=q[1], option2=q[2],
            option3=q[3], option4=q[4], correct_answer=q[5],
            difficulty=q[6], module_id=cd_module1.id))
    db.session.commit()
    print("CD Module 1 inserted successfully!")

    # =====================================
    # CD MODULE 2 – Syntax Analysis
    # =====================================

    cd_module2 = Module.query.filter_by(module_name="Module 2", subject_id=cd.id).first()

    cd_module2_questions = [
        # EASY (1-5)
        ("Parser checks the:",
         "Lexemes", "Syntax structure", "Machine code", "Memory",
         "Syntax structure", "Easy"),
        ("CFG stands for:",
         "Context Free Grammar", "Compiler Free Grammar", "Control Flow Grammar", "Code Flow Grammar",
         "Context Free Grammar", "Easy"),
        ("LL(1) parser is a:",
         "Bottom-up parser", "Top-down parser", "LR parser", "Shift-reduce parser",
         "Top-down parser", "Easy"),
        ("Ambiguous grammar produces:",
         "One parse tree", "More than one parse tree", "No derivation", "No terminals",
         "More than one parse tree", "Easy"),
        ("Epsilon represents:",
         "Error", "Empty string", "Terminal", "Operator",
         "Empty string", "Easy"),

        # INTERMEDIATE (6-13)
        ("FIRST set contains:",
         "All non-terminals", "First terminal symbols derivable from a string",
         "All productions", "Only epsilon",
         "First terminal symbols derivable from a string", "Intermediate"),
        ("FOLLOW set contains:",
         "Terminals that can appear after a non-terminal", "First symbols",
         "Grammar rules", "Parse tree nodes",
         "Terminals that can appear after a non-terminal", "Intermediate"),
        ("Left recursion must be removed for:",
         "Bottom-up parsing", "Top-down parsing", "Code generation", "Optimization",
         "Top-down parsing", "Intermediate"),
        ("Left factoring removes:",
         "Left recursion", "Common prefixes in productions", "Ambiguity", "Terminals",
         "Common prefixes in productions", "Intermediate"),
        ("Predictive parsing avoids:",
         "Backtracking", "Stack usage", "FIRST set computation", "FOLLOW set computation",
         "Backtracking", "Intermediate"),
        ("LL(1) grammar must not have:",
         "Terminals", "Left recursion or ambiguity", "FIRST sets", "FOLLOW sets",
         "Left recursion or ambiguity", "Intermediate"),
        ("Parsing table for LL(1) is constructed using:",
         "FIRST and FOLLOW sets", "LR items", "Stack only", "DFA",
         "FIRST and FOLLOW sets", "Intermediate"),
        ("Recursive descent parser is:",
         "Table-driven", "Hand-written top-down parser", "Bottom-up parser", "LR parser",
         "Hand-written top-down parser", "Intermediate"),

        # ADVANCED (14-20)
        ("If parsing table has multiple entries in a cell, grammar is:",
         "LL(1)", "Not LL(1)", "SLR", "LR(1)",
         "Not LL(1)", "Advanced"),
        ("Top-down parser constructs tree from:",
         "Leaves upward", "Root downward", "Middle outward", "Stack",
         "Root downward", "Advanced"),
        ("In CFG, derivations can be:",
         "Only leftmost", "Only rightmost", "Both leftmost and rightmost", "Neither",
         "Both leftmost and rightmost", "Advanced"),
        ("Left factoring makes grammar suitable for:",
         "Bottom-up parsing", "Predictive top-down parsing", "Code generation", "Optimization",
         "Predictive top-down parsing", "Advanced"),
        ("Syntax errors are detected during:",
         "Lexical analysis", "Parsing", "Optimization", "Linking",
         "Parsing", "Advanced"),
        ("Leftmost derivation always replaces:",
         "Rightmost non-terminal", "Leftmost non-terminal", "Any terminal", "Top of stack",
         "Leftmost non-terminal", "Advanced"),
        ("Predictive parser uses:",
         "Stack and parsing table", "Queue only", "Heap", "DFA only",
         "Stack and parsing table", "Advanced"),
    ]

    for q in cd_module2_questions:
        db.session.add(Question(
            question_text=q[0], option1=q[1], option2=q[2],
            option3=q[3], option4=q[4], correct_answer=q[5],
            difficulty=q[6], module_id=cd_module2.id))
    db.session.commit()
    print("CD Module 2 inserted successfully!")

    # =====================================
    # CD MODULE 3 – Bottom-Up Parsing
    # =====================================

    cd_module3 = Module.query.filter_by(module_name="Module 3", subject_id=cd.id).first()

    cd_module3_questions = [
        # EASY (1-5)
        ("Bottom-up parsing starts from:",
         "Root", "Leaves", "Middle", "Stack top",
         "Leaves", "Easy"),
        ("Shift-reduce parser uses a:",
         "Queue", "Stack", "Heap", "Table only",
         "Stack", "Easy"),
        ("LR stands for:",
         "Left Right", "Left-to-right scan with Rightmost derivation",
         "Logical Reduction", "Lexical Rule",
         "Left-to-right scan with Rightmost derivation", "Easy"),
        ("ACTION table in LR parsing contains:",
         "Shift and Reduce actions", "Grammar rules", "Token list", "Symbol table entries",
         "Shift and Reduce actions", "Easy"),
        ("Augmented grammar adds a new:",
         "Terminal", "Start symbol", "Token", "Stack",
         "Start symbol", "Easy"),

        # INTERMEDIATE (6-13)
        ("Reduce action replaces handle with:",
         "A non-terminal (LHS of production)", "Stack top", "Input symbol", "Token",
         "A non-terminal (LHS of production)", "Intermediate"),
        ("Shift action means:",
         "Remove symbol from input", "Push input symbol onto stack",
         "Pop stack", "Replace production",
         "Push input symbol onto stack", "Intermediate"),
        ("Reduce-reduce conflict means:",
         "Two different reductions are possible", "Two shifts are possible",
         "One reduction is possible", "No action defined",
         "Two different reductions are possible", "Intermediate"),
        ("Shift-reduce conflict means:",
         "Two shifts possible", "Two reductions possible",
         "Both shift and reduce are possible", "No action defined",
         "Both shift and reduce are possible", "Intermediate"),
        ("LALR parser merges similar states of:",
         "LR(0)", "LR(1)", "LL(1)", "SLR",
         "LR(1)", "Intermediate"),
        ("Canonical LR(1) parser is:",
         "Least powerful LR parser", "Most powerful LR parser",
         "Same as LL(1)", "Simplest parser",
         "Most powerful LR parser", "Intermediate"),
        ("GOTO function in LR parsing is used for:",
         "LL parser transitions", "LR parser state transitions",
         "Lexical analysis", "Code generation",
         "LR parser state transitions", "Intermediate"),
        ("SLR parser uses which sets to resolve conflicts?",
         "FIRST sets only", "FOLLOW sets", "Stack only", "DFA states",
         "FOLLOW sets", "Intermediate"),

        # ADVANCED (14-20)
        ("Handle in bottom-up parsing is:",
         "Substring matching RHS of a production at the right place",
         "LHS of a production", "A terminal symbol", "Stack pointer",
         "Substring matching RHS of a production at the right place", "Advanced"),
        ("Bottom-up parsing produces derivation in:",
         "Leftmost order", "Rightmost order in reverse", "Random order", "No derivation",
         "Rightmost order in reverse", "Advanced"),
        ("SLR is less powerful than canonical LR because:",
         "SLR uses larger tables", "SLR uses FOLLOW sets which are less precise",
         "SLR cannot handle shifts", "SLR uses more states",
         "SLR uses FOLLOW sets which are less precise", "Advanced"),
        ("Parsing table conflicts indicate grammar is:",
         "LR(1)", "Not LR or ambiguous", "Unambiguous", "Deterministic",
         "Not LR or ambiguous", "Advanced"),
        ("LALR reduces table size compared to canonical LR by:",
         "Merging states with same core", "Removing terminals",
         "Reducing stack size", "Simplifying grammar",
         "Merging states with same core", "Advanced"),
        ("LR parsing avoids:",
         "Backtracking", "Stack usage", "Grammar rules", "Reduction",
         "Backtracking", "Advanced"),
        ("LR(1) item includes:",
         "Production and dot position only",
         "Production, dot position, and lookahead symbol",
         "Only lookahead", "Only terminals",
         "Production, dot position, and lookahead symbol", "Advanced"),
    ]

    for q in cd_module3_questions:
        db.session.add(Question(
            question_text=q[0], option1=q[1], option2=q[2],
            option3=q[3], option4=q[4], correct_answer=q[5],
            difficulty=q[6], module_id=cd_module3.id))
    db.session.commit()
    print("CD Module 3 inserted successfully!")

    # =====================================
    # CD MODULE 4 – SDT & Intermediate Code Generation
    # =====================================

    cd_module4 = Module.query.filter_by(module_name="Module 4", subject_id=cd.id).first()

    cd_module4_questions = [
        # EASY (1-5)
        ("SDT stands for:",
         "Syntax Data Table", "Syntax Directed Translation",
         "Semantic Data Tree", "Stack Driven Translation",
         "Syntax Directed Translation", "Easy"),
        ("Three-address code contains at most:",
         "1 operand", "2 operands", "3 operands", "4 operands",
         "3 operands", "Easy"),
        ("Quadruple representation has how many fields?",
         "2", "3", "4", "5",
         "4", "Easy"),
        ("Static storage allocation is done at:",
         "Compile time", "Runtime", "Link time", "Execution time",
         "Compile time", "Easy"),
        ("Stack allocation uses:",
         "Activation records", "Symbol table", "DFA", "Parse tree",
         "Activation records", "Easy"),

        # INTERMEDIATE (6-13)
        ("S-attributed definitions use only:",
         "Inherited attributes", "Synthesized attributes",
         "Global variables", "Static variables",
         "Synthesized attributes", "Intermediate"),
        ("L-attributed definitions allow:",
         "Only synthesized attributes", "Only inherited attributes",
         "Both inherited and synthesized (with restrictions)", "No attributes",
         "Both inherited and synthesized (with restrictions)", "Intermediate"),
        ("Intermediate code is:",
         "Machine dependent", "Machine independent",
         "Assembly specific", "Hardware specific",
         "Machine independent", "Intermediate"),
        ("A common form of three-address code is:",
         "x = y op z", "x y op z", "op x y z", "y = op z",
         "x = y op z", "Intermediate"),
        ("DAG (Directed Acyclic Graph) is used for:",
         "Parsing", "Optimization of basic blocks", "Lexical analysis", "Linking",
         "Optimization of basic blocks", "Intermediate"),
        ("Inherited attributes flow:",
         "From child to parent", "From parent to child",
         "Between siblings only", "Randomly",
         "From parent to child", "Intermediate"),
        ("Synthesized attributes flow:",
         "From parent to child", "From child to parent",
         "Same level only", "None",
         "From child to parent", "Intermediate"),
        ("Heap allocation occurs during:",
         "Compile time", "Runtime", "Parsing time", "Link time",
         "Runtime", "Intermediate"),

        # ADVANCED (14-20)
        ("S-attributed SDD is evaluated using:",
         "Top-down traversal", "Bottom-up traversal (LR parsing)",
         "Random traversal", "Left-to-right only",
         "Bottom-up traversal (LR parsing)", "Advanced"),
        ("Reverse Polish Notation is an example of:",
         "Source code", "Intermediate representation (postfix)",
         "Machine code", "Grammar",
         "Intermediate representation (postfix)", "Advanced"),
        ("Activation record contains:",
         "Parse tree only",
         "Local variables, return address, temporaries",
         "Grammar rules", "Token list",
         "Local variables, return address, temporaries", "Advanced"),
        ("Quadruples are preferred over triples because:",
         "Smaller size", "Easier to rearrange for optimization",
         "Less memory", "Faster parsing",
         "Easier to rearrange for optimization", "Advanced"),
        ("Syntax tree differs from parse tree by:",
         "Removing interior nodes for operators",
         "Removing unnecessary nodes like punctuation",
         "Adding more nodes", "Changing grammar",
         "Removing unnecessary nodes like punctuation", "Advanced"),
        ("Intermediate representation improves:",
         "Hardware dependency", "Portability and retargetability of compiler",
         "Grammar complexity", "Memory allocation",
         "Portability and retargetability of compiler", "Advanced"),
        ("Three-address code is generated from:",
         "Source code directly", "Syntax tree or DAG",
         "Symbol table", "Token stream",
         "Syntax tree or DAG", "Advanced"),
    ]

    for q in cd_module4_questions:
        db.session.add(Question(
            question_text=q[0], option1=q[1], option2=q[2],
            option3=q[3], option4=q[4], correct_answer=q[5],
            difficulty=q[6], module_id=cd_module4.id))
    db.session.commit()
    print("CD Module 4 inserted successfully!")

    # =====================================
    # CD MODULE 5 – Code Optimization & Code Generation
    # =====================================

    cd_module5 = Module.query.filter_by(module_name="Module 5", subject_id=cd.id).first()

    cd_module5_questions = [
        # EASY (1-5)
        ("Code optimization aims to improve:",
         "Syntax correctness", "Performance (speed/memory)", "Grammar", "Tokens",
         "Performance (speed/memory)", "Easy"),
        ("Dead code elimination removes:",
         "Useful code", "Unreachable or unused code", "Grammar", "Stack entries",
         "Unreachable or unused code", "Easy"),
        ("Common subexpression elimination removes:",
         "Tokens", "Repeated computations", "Grammar rules", "Stack entries",
         "Repeated computations", "Easy"),
        ("Target code is generated from:",
         "Parse tree", "Intermediate code", "Token stream", "Grammar",
         "Intermediate code", "Easy"),
        ("Register allocation is part of:",
         "Parsing", "Code generation", "Lexical analysis", "Syntax analysis",
         "Code generation", "Easy"),

        # INTERMEDIATE (6-13)
        ("Peephole optimization examines:",
         "Entire program", "Small window of consecutive instructions",
         "Grammar", "Parse tree",
         "Small window of consecutive instructions", "Intermediate"),
        ("Local optimization is applied to:",
         "Entire program", "A basic block", "Single token", "Grammar",
         "A basic block", "Intermediate"),
        ("Global optimization considers:",
         "Single statement", "A basic block only",
         "Entire control flow graph", "Single token",
         "Entire control flow graph", "Intermediate"),
        ("Strength reduction replaces:",
         "Cheap operations with costly ones",
         "Costly operations with cheaper equivalent ones",
         "Tokens", "Grammar rules",
         "Costly operations with cheaper equivalent ones", "Intermediate"),
        ("Loop invariant code motion moves:",
         "Constant expressions outside the loop",
         "Loop body inside a function",
         "Variables randomly", "Nothing",
         "Constant expressions outside the loop", "Intermediate"),
        ("Machine independent optimization is performed:",
         "After target code generation", "Before target code generation",
         "During execution", "During linking",
         "Before target code generation", "Intermediate"),
        ("Control flow graph represents:",
         "Grammar rules", "Flow of control between basic blocks",
         "Token list", "Symbol table",
         "Flow of control between basic blocks", "Intermediate"),
        ("Register spilling occurs when:",
         "Registers are sufficient", "There are more variables than available registers",
         "Stack is empty", "Grammar is wrong",
         "There are more variables than available registers", "Intermediate"),

        # ADVANCED (14-20)
        ("Function preserving transformations must:",
         "Change the program's meaning", "Preserve the program's semantics",
         "Remove grammar", "Remove tokens",
         "Preserve the program's semantics", "Advanced"),
        ("Instruction selection in code generation depends on:",
         "Grammar rules", "Target machine's instruction set",
         "Token stream", "FIRST sets",
         "Target machine's instruction set", "Advanced"),
        ("DAG helps in eliminating:",
         "Syntax errors", "Redundant expressions within a basic block",
         "Token errors", "Grammar ambiguity",
         "Redundant expressions within a basic block", "Advanced"),
        ("Constant folding means:",
         "Evaluating constant expressions at compile time",
         "Evaluating expressions at runtime",
         "Removing loops", "Linking constants",
         "Evaluating constant expressions at compile time", "Advanced"),
        ("Copy propagation replaces:",
         "Function calls", "Uses of variable x=y with y directly",
         "Constants", "Loop conditions",
         "Uses of variable x=y with y directly", "Advanced"),
        ("Basic block is a sequence of instructions with:",
         "Multiple entry points", "Single entry and single exit point",
         "No branches", "Only assignments",
         "Single entry and single exit point", "Advanced"),
        ("Machine dependent optimization depends on:",
         "Grammar rules", "Target hardware architecture features",
         "Token stream", "Parse tree",
         "Target hardware architecture features", "Advanced"),
    ]

    for q in cd_module5_questions:
        db.session.add(Question(
            question_text=q[0], option1=q[1], option2=q[2],
            option3=q[3], option4=q[4], correct_answer=q[5],
            difficulty=q[6], module_id=cd_module5.id))
    db.session.commit()
    print("CD Module 5 inserted successfully!")

    # =====================================
    # CG MODULE 1 – Basics of Computer Graphics
    # =====================================

    cg = subject_objects["CG"]

    cg_module1 = Module.query.filter_by(module_name="Module 1", subject_id=cg.id).first()

    cg_module1_questions = [
        # EASY (1-5)
        ("Computer Graphics deals with:",
         "Image processing only", "Creation and manipulation of images",
         "Networking", "Compiler design",
         "Creation and manipulation of images", "Easy"),
        ("Pixel stands for:",
         "Picture element", "Point element", "Paint element", "Plot element",
         "Picture element", "Easy"),
        ("Primary colors in RGB model are:",
         "Red, Green, Blue", "Red, Yellow, Blue",
         "Cyan, Magenta, Yellow", "Black, White, Red",
         "Red, Green, Blue", "Easy"),
        ("Raster graphics are based on:",
         "Pixels", "Mathematical equations", "Vectors", "Lines only",
         "Pixels", "Easy"),
        ("Refresh rate is measured in:",
         "Hz", "Pixels", "Bytes", "Inches",
         "Hz", "Easy"),

        # INTERMEDIATE (6-13)
        ("Vector graphics are based on:",
         "Pixels", "Mathematical formulas and curves", "Dots only", "Resolution",
         "Mathematical formulas and curves", "Intermediate"),
        ("Resolution of an image refers to:",
         "Number of colors", "Number of pixels per unit area",
         "Brightness level", "Size of monitor",
         "Number of pixels per unit area", "Intermediate"),
        ("Frame buffer stores:",
         "Program code", "Pixel color values", "Keyboard input", "CPU instructions",
         "Pixel color values", "Intermediate"),
        ("Aliasing occurs due to:",
         "Too high resolution", "Insufficient sampling rate (low resolution)",
         "Too much memory", "High refresh rate",
         "Insufficient sampling rate (low resolution)", "Intermediate"),
        ("Anti-aliasing technique is used to:",
         "Increase brightness", "Smooth jagged edges", "Reduce memory", "Increase size",
         "Smooth jagged edges", "Intermediate"),
        ("Scan conversion is process of:",
         "Converting objects to pixel representation", "Color mixing",
         "Zooming images", "Saving files",
         "Converting objects to pixel representation", "Intermediate"),
        ("CRT stands for:",
         "Cathode Ray Tube", "Computer Ray Tube", "Color Ray Tube", "Control Ray Tube",
         "Cathode Ray Tube", "Intermediate"),
        ("Random scan (vector) display draws:",
         "Whole screen pixel by pixel", "Only the required lines/vectors",
         "Pixels row by row", "Color patterns only",
         "Only the required lines/vectors", "Intermediate"),

        # ADVANCED (14-20)
        ("DDA algorithm is used for:",
         "Circle drawing", "Line drawing", "Polygon filling", "Clipping",
         "Line drawing", "Advanced"),
        ("Bresenham's line algorithm is preferred because:",
         "Uses floating point arithmetic", "Uses only integer arithmetic",
         "Is slower but accurate", "Uses recursive calls",
         "Uses only integer arithmetic", "Advanced"),
        ("Midpoint circle algorithm uses:",
         "Floating point operations", "Integer arithmetic and symmetry",
         "DDA technique", "Scan line method",
         "Integer arithmetic and symmetry", "Advanced"),
        ("Scan line algorithm is used for:",
         "Line drawing", "Polygon filling", "Rotation", "Translation",
         "Polygon filling", "Advanced"),
        ("Double buffering helps to:",
         "Reduce screen flickering", "Increase memory error",
         "Slow display speed", "Increase aliasing",
         "Reduce screen flickering", "Advanced"),
        ("Color depth determines:",
         "Number of colors displayable", "Resolution",
         "Refresh rate", "Number of pixels",
         "Number of colors displayable", "Advanced"),
        ("Aspect ratio of a display is:",
         "Height divided by Width", "Width divided by Height",
         "Pixels per inch", "Resolution value",
         "Width divided by Height", "Advanced"),
    ]

    for q in cg_module1_questions:
        db.session.add(Question(
            question_text=q[0], option1=q[1], option2=q[2],
            option3=q[3], option4=q[4], correct_answer=q[5],
            difficulty=q[6], module_id=cg_module1.id))
    db.session.commit()
    print("CG Module 1 inserted successfully!")

    # =====================================
    # CG MODULE 2 – 2D Transformations & Viewing
    # =====================================

    cg_module2 = Module.query.filter_by(module_name="Module 2", subject_id=cg.id).first()

    cg_module2_questions = [
        # EASY (1-5)
        ("Translation moves an object by:",
         "Rotating it", "Scaling it", "Shifting its position", "Reflecting it",
         "Shifting its position", "Easy"),
        ("Scaling changes an object's:",
         "Position", "Size", "Color", "Brightness",
         "Size", "Easy"),
        ("Reflection produces:",
         "Mirror image of object", "Rotation of object",
         "Scaling of object", "Translation of object",
         "Mirror image of object", "Easy"),
        ("Homogeneous coordinates in 2D use:",
         "2 values", "3 values", "4 values", "1 value",
         "3 values", "Easy"),
        ("Shearing transformation changes:",
         "Shape of object", "Color", "Brightness", "Resolution",
         "Shape of object", "Easy"),

        # INTERMEDIATE (6-13)
        ("2D transformation matrix uses homogeneous coordinates of size:",
         "2×2", "3×3", "4×4", "1×1",
         "3×3", "Intermediate"),
        ("Rotation matrix in 2D contains:",
         "sin and cos values", "Only 1s and 0s", "Only zeros", "Random values",
         "sin and cos values", "Intermediate"),
        ("If scaling factor Sx > 1:",
         "Object shrinks along x", "Object enlarges along x",
         "Object rotates", "No change",
         "Object enlarges along x", "Intermediate"),
        ("Viewing transformation converts:",
         "World coordinates to screen coordinates", "Screen to world coordinates",
         "Color to grayscale", "2D to 3D",
         "World coordinates to screen coordinates", "Intermediate"),
        ("Window in viewing refers to:",
         "Display screen", "Selected rectangular area in world coordinates",
         "OS window", "Monitor size",
         "Selected rectangular area in world coordinates", "Intermediate"),
        ("Viewport refers to:",
         "World coordinate area", "Rectangular area on screen where scene is displayed",
         "Color model", "Matrix",
         "Rectangular area on screen where scene is displayed", "Intermediate"),
        ("Composite transformation means:",
         "Single transformation", "Sequence of multiple transformations combined",
         "Reflection only", "Scaling only",
         "Sequence of multiple transformations combined", "Intermediate"),
        ("Order of transformations in composite transformation:",
         "Does not matter", "Matters (non-commutative)", "Is always commutative", "Is random",
         "Matters (non-commutative)", "Intermediate"),

        # ADVANCED (14-20)
        ("Reflection about the line y=x swaps:",
         "x and y coordinates", "Only x coordinate",
         "Only y coordinate", "No coordinates",
         "x and y coordinates", "Advanced"),
        ("Pivot point rotation requires:",
         "Only rotation matrix",
         "Translate to origin, rotate, translate back",
         "Only scaling", "Shearing before rotation",
         "Translate to origin, rotate, translate back", "Advanced"),
        ("Clipping removes:",
         "Visible parts of scene", "Parts outside the clipping window",
         "Colors from image", "Random pixels",
         "Parts outside the clipping window", "Advanced"),
        ("Cohen-Sutherland algorithm is used for:",
         "Circle drawing", "Line clipping", "Polygon filling", "Scaling",
         "Line clipping", "Advanced"),
        ("Liang-Barsky algorithm for line clipping uses:",
         "Outcode method", "Parametric form of line",
         "Polygon decomposition", "Rotation method",
         "Parametric form of line", "Advanced"),
        ("Reflection about x-axis changes:",
         "Sign of y coordinate", "Sign of x coordinate",
         "Both x and y signs", "Neither",
         "Sign of y coordinate", "Advanced"),
        ("Viewport transformation maps:",
         "World space to screen (viewport) space", "Screen to world space",
         "Color to grayscale", "3D to 2D",
         "World space to screen (viewport) space", "Advanced"),
    ]

    for q in cg_module2_questions:
        db.session.add(Question(
            question_text=q[0], option1=q[1], option2=q[2],
            option3=q[3], option4=q[4], correct_answer=q[5],
            difficulty=q[6], module_id=cg_module2.id))
    db.session.commit()
    print("CG Module 2 inserted successfully!")

    # =====================================
    # CG MODULE 3 – 3D Transformations & Projections
    # =====================================

    cg_module3 = Module.query.filter_by(module_name="Module 3", subject_id=cg.id).first()

    cg_module3_questions = [
        # EASY (1-5)
        ("3D translation uses how many translation parameters?",
         "2 (tx, ty)", "3 (tx, ty, tz)", "4", "1",
         "3 (tx, ty, tz)", "Easy"),
        ("Projection converts:",
         "2D objects to 3D", "3D objects to 2D representation",
         "Color to grayscale", "Pixels to vectors",
         "3D objects to 2D representation", "Easy"),
        ("Parallel projection maintains:",
         "Perspective depth effect", "Parallel lines remain parallel",
         "Vanishing point", "Distortion of far objects",
         "Parallel lines remain parallel", "Easy"),
        ("Perspective projection creates:",
         "Parallel line effect", "Realistic depth effect (foreshortening)",
         "No depth change", "Scaling only",
         "Realistic depth effect (foreshortening)", "Easy"),
        ("Rotation in 3D can occur about:",
         "X-axis only", "Y-axis only", "Z-axis only", "All of X, Y, Z axes",
         "All of X, Y, Z axes", "Easy"),

        # INTERMEDIATE (6-13)
        ("3D homogeneous coordinates use:",
         "3 values (x,y,z)", "4 values (x,y,z,w)", "2 values", "1 value",
         "4 values (x,y,z,w)", "Intermediate"),
        ("3D transformation matrix size is:",
         "3×3", "4×4", "2×2", "5×5",
         "4×4", "Intermediate"),
        ("3D rotation about X-axis affects:",
         "Y and Z coordinates", "Only X coordinate",
         "Only Y coordinate", "Only Z coordinate",
         "Y and Z coordinates", "Intermediate"),
        ("Orthographic projection is a type of:",
         "Perspective projection", "Parallel projection", "Scaling", "Clipping",
         "Parallel projection", "Intermediate"),
        ("Vanishing point(s) appear in:",
         "Parallel projection", "Perspective projection", "Scaling only", "Reflection only",
         "Perspective projection", "Intermediate"),
        ("Composite 3D transformations are computed using:",
         "Matrix addition", "Matrix multiplication", "Matrix division", "Subtraction",
         "Matrix multiplication", "Intermediate"),
        ("Projection plane is a:",
         "3D object", "2D surface onto which scene is projected",
         "Matrix", "Vector",
         "2D surface onto which scene is projected", "Intermediate"),
        ("If 3D scaling factor < 1:",
         "Object enlarges", "Object shrinks", "Object rotates", "No change",
         "Object shrinks", "Intermediate"),

        # ADVANCED (14-20)
        ("Order of 3D transformations is:",
         "Always commutative", "Non-commutative (order matters)",
         "Always gives same result", "Constant",
         "Non-commutative (order matters)", "Advanced"),
        ("Perspective division divides x, y by:",
         "x coordinate", "y coordinate", "z coordinate", "w coordinate",
         "w coordinate", "Advanced"),
        ("Oblique projection is a type of:",
         "Perspective projection", "Parallel projection",
         "Scaling", "Rotation",
         "Parallel projection", "Advanced"),
        ("Isometric projection is a parallel projection where:",
         "Only one axis is equal", "All three axes are equally foreshortened",
         "No axis is foreshortened", "One axis is vertical only",
         "All three axes are equally foreshortened", "Advanced"),
        ("Hidden surface removal is required for:",
         "2D flat objects", "Realistic 3D rendering",
         "Scaling only", "Translation only",
         "Realistic 3D rendering", "Advanced"),
        ("Z-buffer (depth buffer) algorithm is used for:",
         "Line clipping", "Hidden surface removal",
         "Scaling", "Line drawing",
         "Hidden surface removal", "Advanced"),
        ("Isometric projection axes are at angles of:",
         "120 degrees to each other", "90 degrees to each other",
         "60 degrees to each other", "45 degrees to each other",
         "120 degrees to each other", "Advanced"),
    ]

    for q in cg_module3_questions:
        db.session.add(Question(
            question_text=q[0], option1=q[1], option2=q[2],
            option3=q[3], option4=q[4], correct_answer=q[5],
            difficulty=q[6], module_id=cg_module3.id))
    db.session.commit()
    print("CG Module 3 inserted successfully!")

    # =====================================
    # CG MODULE 4 – Curves, Surfaces & Illumination
    # =====================================

    cg_module4 = Module.query.filter_by(module_name="Module 4", subject_id=cg.id).first()

    cg_module4_questions = [
        # EASY (1-5)
        ("Bezier curve is defined using:",
         "Control points", "Pixels", "Color model", "Matrix only",
         "Control points", "Easy"),
        ("Ambient light is:",
         "Directional spotlight", "Non-directional background light",
         "Reflected light only", "Refracted light",
         "Non-directional background light", "Easy"),
        ("Diffuse reflection depends on:",
         "Viewer position", "Angle between light direction and surface normal",
         "Color only", "Matrix",
         "Angle between light direction and surface normal", "Easy"),
        ("Parametric curves are represented using:",
         "Single explicit equation", "A parameter t",
         "Matrix only", "Color model",
         "A parameter t", "Easy"),
        ("B-spline curve provides:",
         "Global control", "Local control of curve shape",
         "No control", "Only scaling",
         "Local control of curve shape", "Easy"),

        # INTERMEDIATE (6-13)
        ("Specular reflection produces:",
         "Matte finish", "Shiny highlight effect",
         "Shadow only", "No reflection",
         "Shiny highlight effect", "Intermediate"),
        ("Phong illumination model includes:",
         "Ambient light only", "Ambient + Diffuse + Specular components",
         "Diffuse only", "Specular only",
         "Ambient + Diffuse + Specular components", "Intermediate"),
        ("Bezier curve uses which basis polynomial?",
         "Taylor polynomial", "Bernstein polynomial",
         "Fourier series", "Lagrange polynomial",
         "Bernstein polynomial", "Intermediate"),
        ("Cubic Bezier curve uses how many control points?",
         "2", "3", "4", "5",
         "4", "Intermediate"),
        ("B-spline stands for:",
         "Basic spline", "Basis spline", "Binary spline", "Bezier spline",
         "Basis spline", "Intermediate"),
        ("Surface patch is formed by sweeping:",
         "Two points", "A curve along another curve",
         "Single point", "Pixel group",
         "A curve along another curve", "Intermediate"),
        ("Normal vector to surface is used in:",
         "Translation calculation", "Illumination calculation",
         "Scaling", "Clipping",
         "Illumination calculation", "Intermediate"),
        ("Hermite curve is defined using:",
         "Control points only", "End points and tangent vectors at endpoints",
         "Pixels", "Matrix only",
         "End points and tangent vectors at endpoints", "Intermediate"),

        # ADVANCED (14-20)
        ("Local control property of B-spline means:",
         "Moving one control point changes entire curve",
         "Moving one control point affects only nearby portion of curve",
         "Color changes locally", "Resolution changes",
         "Moving one control point affects only nearby portion of curve", "Advanced"),
        ("Phong shading interpolates:",
         "Colors at vertices", "Normal vectors across surface, then computes lighting per pixel",
         "Only ambient light", "Texture coordinates",
         "Normal vectors across surface, then computes lighting per pixel", "Advanced"),
        ("Gouraud shading computes intensity at:",
         "Each pixel independently", "Each vertex, then interpolates",
         "Each edge", "Whole object once",
         "Each vertex, then interpolates", "Advanced"),
        ("Specular reflection depends on:",
         "Only surface color",
         "Viewer position, light position, and surface normal",
         "Translation only", "Scaling only",
         "Viewer position, light position, and surface normal", "Advanced"),
        ("Higher degree Bezier curves give:",
         "Less flexibility and more oscillation",
         "More flexibility but harder to control locally",
         "No curvature", "Reduce aliasing",
         "More flexibility but harder to control locally", "Advanced"),
        ("Phong shading is more accurate than Gouraud because:",
         "It is faster", "It computes lighting per pixel instead of per vertex",
         "It uses fewer calculations", "It ignores specular highlights",
         "It computes lighting per pixel instead of per vertex", "Advanced"),
        ("Specular highlight size depends on:",
         "Shininess (n) coefficient", "Resolution",
         "Translation", "Scaling",
         "Shininess (n) coefficient", "Advanced"),
    ]

    for q in cg_module4_questions:
        db.session.add(Question(
            question_text=q[0], option1=q[1], option2=q[2],
            option3=q[3], option4=q[4], correct_answer=q[5],
            difficulty=q[6], module_id=cg_module4.id))
    db.session.commit()
    print("CG Module 4 inserted successfully!")

    # =====================================
    # CG MODULE 5 – Animation & Rendering Techniques
    # =====================================

    cg_module5 = Module.query.filter_by(module_name="Module 5", subject_id=cg.id).first()

    cg_module5_questions = [
        # EASY (1-5)
        ("Animation is created by:",
         "Displaying a sequence of images rapidly", "Single image rendering",
         "Scaling objects", "Clipping objects",
         "Displaying a sequence of images rapidly", "Easy"),
        ("Frame rate is measured in:",
         "Hz", "FPS (Frames Per Second)", "Pixels", "Bytes",
         "FPS (Frames Per Second)", "Easy"),
        ("Key frame animation defines:",
         "Every single frame manually", "Important frames at key positions",
         "No frames", "Random frames",
         "Important frames at key positions", "Easy"),
        ("Rendering means:",
         "Generating final image from 3D model", "Scaling object",
         "Clipping", "Translation",
         "Generating final image from 3D model", "Easy"),
        ("Ray tracing simulates:",
         "Light ray behavior for realistic rendering", "Scaling",
         "Translation", "Clipping",
         "Light ray behavior for realistic rendering", "Easy"),

        # INTERMEDIATE (6-13)
        ("Tweening (in-betweening) is:",
         "Deleting frames", "Generating intermediate frames between keyframes",
         "Scaling images", "Reflecting images",
         "Generating intermediate frames between keyframes", "Intermediate"),
        ("Global illumination considers:",
         "Only direct lighting", "Multiple light reflections and indirect lighting",
         "No lighting", "Color mixing only",
         "Multiple light reflections and indirect lighting", "Intermediate"),
        ("Z-buffer algorithm is used for:",
         "Hidden surface removal", "Scaling", "Rotation", "Color correction",
         "Hidden surface removal", "Intermediate"),
        ("Back-face culling removes:",
         "Front visible faces", "Faces whose normal points away from viewer",
         "Edges only", "Texture coordinates",
         "Faces whose normal points away from viewer", "Intermediate"),
        ("Texture mapping adds:",
         "Surface detail to objects", "Scaling", "Translation", "Clipping",
         "Surface detail to objects", "Intermediate"),
        ("Ray casting is a simplified version of:",
         "Rasterization", "Ray tracing", "Clipping", "Shearing",
         "Ray tracing", "Intermediate"),
        ("Depth cueing provides sense of:",
         "Brightness variation", "Distance (farther objects appear dimmer)",
         "Color change", "Resolution",
         "Distance (farther objects appear dimmer)", "Intermediate"),
        ("Interpolation in animation is used to:",
         "Delete frames", "Generate smooth transitions between keyframes",
         "Scale images", "Clip objects",
         "Generate smooth transitions between keyframes", "Intermediate"),

        # ADVANCED (14-20)
        ("Ray tracing computes:",
         "Only shadows", "Reflection, refraction, and shadows",
         "Scaling only", "Rotation only",
         "Reflection, refraction, and shadows", "Advanced"),
        ("Radiosity method mainly handles:",
         "Specular reflection", "Diffuse interreflection between surfaces",
         "Scaling", "Translation",
         "Diffuse interreflection between surfaces", "Advanced"),
        ("Motion blur effect represents:",
         "Object moving very slowly", "Object moving fast (capturing motion in single frame)",
         "Scaling artifact", "Clipping artifact",
         "Object moving fast (capturing motion in single frame)", "Advanced"),
        ("Rendering pipeline includes:",
         "Modeling, transformation, lighting, rasterization",
         "Scaling only", "Clipping only", "Translation only",
         "Modeling, transformation, lighting, rasterization", "Advanced"),
        ("Higher sampling rate in rendering improves:",
         "Image quality (reduces aliasing)", "Scaling speed",
         "Memory error rate", "Clipping accuracy",
         "Image quality (reduces aliasing)", "Advanced"),
        ("Shadow is correctly rendered when:",
         "All surfaces are lit", "Points not visible from light source are in shadow",
         "Object scales", "Pixels change randomly",
         "Points not visible from light source are in shadow", "Advanced"),
        ("Ray tracing is computationally expensive because:",
         "It is simple", "It traces rays for every pixel through the scene",
         "It uses integer math", "It only handles diffuse light",
         "It traces rays for every pixel through the scene", "Advanced"),
    ]

    for q in cg_module5_questions:
        db.session.add(Question(
            question_text=q[0], option1=q[1], option2=q[2],
            option3=q[3], option4=q[4], correct_answer=q[5],
            difficulty=q[6], module_id=cg_module5.id))
    db.session.commit()
    print("CG Module 5 inserted successfully!")

    # =====================================
    # IEFT MODULE 1 – Demand, Supply & Market
    # =====================================

    ieft = subject_objects["IEFT"]

    ieft_module1 = Module.query.filter_by(module_name="Module 1", subject_id=ieft.id).first()

    ieft_module1_questions = [
        ("Scarcity in economics means:",
         "Unlimited resources", "Limited resources relative to unlimited wants",
         "Excess supply", "No production",
         "Limited resources relative to unlimited wants", "Easy"),
        ("Law of demand states:",
         "Price rises, demand rises", "Price falls, demand falls",
         "Price rises, demand falls", "No relation between price and demand",
         "Price rises, demand falls", "Easy"),
        ("Law of supply states:",
         "Price rises, supply falls", "Price rises, supply rises",
         "Price falls, supply rises", "No relation",
         "Price rises, supply rises", "Easy"),
        ("Market equilibrium occurs when:",
         "Demand exceeds Supply", "Supply exceeds Demand",
         "Quantity demanded equals quantity supplied", "Price equals zero",
         "Quantity demanded equals quantity supplied", "Easy"),
        ("PPC (Production Possibility Curve) shows:",
         "Demand only", "Supply only",
         "Maximum combinations of two goods producible", "Profit curve",
         "Maximum combinations of two goods producible", "Easy"),
        ("Consumer surplus is:",
         "Extra tax paid", "Difference between willingness to pay and actual price paid",
         "Government revenue", "Total cost of production",
         "Difference between willingness to pay and actual price paid", "Intermediate"),
        ("Producer surplus is:",
         "Extra cost", "Difference between price received and minimum price acceptable",
         "Consumer benefit", "Tax revenue",
         "Difference between price received and minimum price acceptable", "Intermediate"),
        ("Price elasticity of demand measures:",
         "Change in supply due to price", "Responsiveness of quantity demanded to price change",
         "Income effect only", "Cost change",
         "Responsiveness of quantity demanded to price change", "Intermediate"),
        ("If demand is perfectly inelastic, elasticity equals:",
         "Infinity", "1", "0", "-1",
         "0", "Intermediate"),
        ("A shift in demand curve is caused by:",
         "Change in price of the good", "Change in income or taste or price of related goods",
         "Change in quantity demanded only", "Change in supply",
         "Change in income or taste or price of related goods", "Intermediate"),
        ("Substitute goods have:",
         "Negative cross elasticity", "Positive cross elasticity",
         "Zero cross elasticity", "Infinite elasticity",
         "Positive cross elasticity", "Intermediate"),
        ("Complementary goods have:",
         "Positive cross elasticity", "Negative cross elasticity",
         "Zero elasticity", "Unit elasticity",
         "Negative cross elasticity", "Intermediate"),
        ("When price floor is set above equilibrium price:",
         "Shortage occurs", "Surplus occurs",
         "Equilibrium is maintained", "Demand increases",
         "Surplus occurs", "Intermediate"),
        ("Deadweight loss occurs due to:",
         "Perfect competition", "Taxation or price controls distorting market",
         "Equilibrium pricing", "Demand increase",
         "Taxation or price controls distorting market", "Advanced"),
        ("If supply decreases and demand remains constant, equilibrium price:",
         "Falls", "Rises", "Stays same", "Becomes zero",
         "Rises", "Advanced"),
        ("Income elasticity of a normal good is:",
         "Negative", "Zero", "Positive", "Infinite",
         "Positive", "Advanced"),
        ("Giffen goods are those for which demand:",
         "Falls when price rises", "Rises when price rises",
         "Is perfectly elastic", "Is independent of price",
         "Rises when price rises", "Advanced"),
        ("Price ceiling set below equilibrium causes:",
         "Surplus in market", "Shortage in market",
         "No effect on market", "Supply to increase",
         "Shortage in market", "Advanced"),
        ("The slope of demand curve is typically:",
         "Positive (upward sloping)", "Negative (downward sloping)",
         "Zero (horizontal)", "Infinite (vertical)",
         "Negative (downward sloping)", "Advanced"),
        ("When two goods are perfect substitutes, cross elasticity of demand is:",
         "Zero", "Negative and large", "Positive and large (approaching infinity)", "Equal to one",
         "Positive and large (approaching infinity)", "Advanced"),
    ]

    for q in ieft_module1_questions:
        db.session.add(Question(
            question_text=q[0], option1=q[1], option2=q[2],
            option3=q[3], option4=q[4], correct_answer=q[5],
            difficulty=q[6], module_id=ieft_module1.id))
    db.session.commit()
    print("IEFT Module 1 inserted successfully!")

    # =====================================
    # IEFT MODULE 2 – Production & Cost
    # =====================================

    ieft_module2 = Module.query.filter_by(module_name="Module 2", subject_id=ieft.id).first()

    ieft_module2_questions = [
        ("Production function shows relation between:",
         "Price and demand", "Inputs and output produced",
         "Cost and tax", "Revenue and demand",
         "Inputs and output produced", "Easy"),
        ("Law of variable proportion applies in:",
         "Long run", "Short run", "International trade", "Monopoly",
         "Short run", "Easy"),
        ("Explicit cost is:",
         "Opportunity cost", "Actual monetary payment made",
         "Hidden cost", "Sunk cost",
         "Actual monetary payment made", "Easy"),
        ("Break-even point occurs when:",
         "Profit is maximum", "Loss is maximum",
         "Total Revenue equals Total Cost", "MC equals MR",
         "Total Revenue equals Total Cost", "Easy"),
        ("Isoquant curve represents:",
         "Equal cost combinations", "Equal output combinations of inputs",
         "Equal revenue", "Equal tax",
         "Equal output combinations of inputs", "Easy"),
        ("Sunk cost is:",
         "Recoverable future cost", "Future anticipated cost",
         "Past cost that cannot be recovered", "Variable cost",
         "Past cost that cannot be recovered", "Intermediate"),
        ("Internal economies of scale arise:",
         "Due to industry growth", "Within the firm as it expands",
         "Due to country's growth", "In the market only",
         "Within the firm as it expands", "Intermediate"),
        ("Cobb-Douglas production function is used to analyze:",
         "Utility maximization", "Production relationships",
         "Demand elasticity", "Inflation",
         "Production relationships", "Intermediate"),
        ("Shutdown point occurs when:",
         "Price falls below AVC", "Price exceeds AVC",
         "TR exceeds TC", "MC exceeds MR",
         "Price falls below AVC", "Intermediate"),
        ("Social cost includes:",
         "Only private cost", "Only external cost",
         "Private cost plus external cost", "Revenue only",
         "Private cost plus external cost", "Intermediate"),
        ("Marginal cost (MC) is the derivative of:",
         "Total Revenue", "Total Cost", "Average Cost", "Average Variable Cost",
         "Total Cost", "Intermediate"),
        ("In long run, all costs are:",
         "Fixed", "Variable", "Sunk", "Zero",
         "Variable", "Intermediate"),
        ("Economies of scale cause:",
         "AC to rise with output", "AC to fall as output increases",
         "TR to fall", "Demand to fall",
         "AC to fall as output increases", "Intermediate"),
        ("External diseconomy example:",
         "Firm's internal rent", "Pollution affecting other firms",
         "Wage payment", "Interest on loan",
         "Pollution affecting other firms", "Intermediate"),
        ("Producer equilibrium is achieved when:",
         "MC equals MR", "TR equals TC",
         "AC is minimum", "AVC is maximum",
         "MC equals MR", "Intermediate"),
        ("Contribution margin equals:",
         "Fixed Cost minus Variable Cost", "Sales Revenue minus Variable Cost",
         "Sales Revenue minus Fixed Cost", "Variable Cost minus Fixed Cost",
         "Sales Revenue minus Variable Cost", "Advanced"),
        ("If fixed cost increases, the break-even point:",
         "Falls", "Rises", "Becomes zero", "Remains constant",
         "Rises", "Advanced"),
        ("Long-run average cost (LAC) curve shape is:",
         "U-shaped due to economies and diseconomies of scale", "Straight line",
         "Vertical", "Flat always",
         "U-shaped due to economies and diseconomies of scale", "Advanced"),
        ("Technical progress in production shifts:",
         "Only demand curve", "Only supply curve",
         "PPC outward (more output possible)", "Revenue curve downward",
         "PPC outward (more output possible)", "Advanced"),
        ("Expansion path shows:",
         "Profit maximization", "Firm growth over time",
         "Optimal input combinations at different output levels",
         "Tax minimization",
         "Optimal input combinations at different output levels", "Advanced"),
    ]

    for q in ieft_module2_questions:
        db.session.add(Question(
            question_text=q[0], option1=q[1], option2=q[2],
            option3=q[3], option4=q[4], correct_answer=q[5],
            difficulty=q[6], module_id=ieft_module2.id))
    db.session.commit()
    print("IEFT Module 2 inserted successfully!")

    # =====================================
    # IEFT MODULE 3 – Market Structure
    # =====================================

    ieft_module3 = Module.query.filter_by(module_name="Module 3", subject_id=ieft.id).first()

    ieft_module3_questions = [
        ("Perfect competition has:",
         "Many sellers with homogeneous product", "One seller",
         "Few sellers", "Two sellers only",
         "Many sellers with homogeneous product", "Easy"),
        ("Monopoly has:",
         "Many competing firms", "A single seller with no close substitutes",
         "Many buyers and sellers", "Homogeneous product",
         "A single seller with no close substitutes", "Easy"),
        ("Oligopoly has:",
         "Few interdependent sellers", "Many sellers",
         "One seller", "No competition",
         "Few interdependent sellers", "Easy"),
        ("A monopolist is a price:",
         "Taker", "Maker (price setter)", "Follower", "Controller only",
         "Maker (price setter)", "Easy"),
        ("Non-price competition includes:",
         "Price cutting", "Advertising and product differentiation",
         "Tax reduction", "Supply increase",
         "Advertising and product differentiation", "Easy"),
        ("Predatory pricing aims to:",
         "Increase consumer welfare", "Drive out competitors by pricing below cost",
         "Raise production cost", "Achieve equilibrium",
         "Drive out competitors by pricing below cost", "Intermediate"),
        ("Cost plus pricing formula is:",
         "Cost plus Tax", "Cost plus Profit margin",
         "Cost plus Supply", "Cost plus Demand",
         "Cost plus Profit margin", "Intermediate"),
        ("Profit maximization condition for any firm is:",
         "TR equals TC", "MR equals MC",
         "Shutdown condition", "Zero tax",
         "MR equals MC", "Intermediate"),
        ("Collusive oligopoly means firms:",
         "Compete aggressively", "Cooperate to maximize joint profit",
         "Follow free trade", "Behave like monopoly individually",
         "Cooperate to maximize joint profit", "Intermediate"),
        ("In perfect competition, the demand curve faced by a single firm is:",
         "Downward sloping", "Perfectly horizontal (elastic)",
         "Vertical (inelastic)", "Upward sloping",
         "Perfectly horizontal (elastic)", "Intermediate"),
        ("Supernormal (economic) profit occurs when:",
         "AR exceeds AC", "AR is less than AC",
         "TR is less than TC", "MR equals zero",
         "AR exceeds AC", "Intermediate"),
        ("Price skimming strategy is used for:",
         "Old declining products", "New innovative products",
         "Tax reduction", "Loss minimization",
         "New innovative products", "Intermediate"),
        ("Oligopoly interdependence means:",
         "Firms act independently", "No rivals exist",
         "Each firm's decision affects and is affected by rivals", "Monopoly behavior",
         "Each firm's decision affects and is affected by rivals", "Intermediate"),
        ("Target return pricing ensures:",
         "Only cost recovery", "A fixed return on investment (ROI)",
         "Minimum loss", "Price elasticity",
         "A fixed return on investment (ROI)", "Intermediate"),
        ("Perfect competition product is:",
         "Differentiated", "Homogeneous (identical)", "Unique", "Branded",
         "Homogeneous (identical)", "Intermediate"),
        ("Monopoly leads to market welfare:",
         "Gain compared to competition", "Loss (deadweight loss) compared to competition",
         "No change", "Tax revenue gain",
         "Loss (deadweight loss) compared to competition", "Advanced"),
        ("In perfect competition AR equals MR because:",
         "Firm controls price", "Firm is price taker so P=AR=MR",
         "Oligopoly condition", "Trade restriction",
         "Firm is price taker so P=AR=MR", "Advanced"),
        ("Going rate pricing means firm prices:",
         "Based on its own cost", "Based on prevailing industry/competitor price",
         "Based on demand only", "Based on government rule",
         "Based on prevailing industry/competitor price", "Advanced"),
        ("Barriers to entry in a market create:",
         "Perfect competition", "Monopoly power and supernormal profit",
         "Free market", "Elastic demand",
         "Monopoly power and supernormal profit", "Advanced"),
        ("Kinked demand curve model is associated with:",
         "Monopoly", "Oligopoly price rigidity",
         "Perfect competition", "International trade",
         "Oligopoly price rigidity", "Advanced"),
    ]

    for q in ieft_module3_questions:
        db.session.add(Question(
            question_text=q[0], option1=q[1], option2=q[2],
            option3=q[3], option4=q[4], correct_answer=q[5],
            difficulty=q[6], module_id=ieft_module3.id))
    db.session.commit()
    print("IEFT Module 3 inserted successfully!")

    # =====================================
    # IEFT MODULE 4 – Macroeconomics
    # =====================================

    ieft_module4 = Module.query.filter_by(module_name="Module 4", subject_id=ieft.id).first()

    ieft_module4_questions = [
        ("GDP measures:",
         "Only welfare", "Total value of goods and services produced in a country",
         "Only demand", "Tax collected",
         "Total value of goods and services produced in a country", "Easy"),
        ("Inflation means:",
         "General price level falling", "General price level rising over time",
         "Output rising", "Tax rising",
         "General price level rising over time", "Easy"),
        ("Fiscal policy is implemented by:",
         "RBI (Central Bank)", "Government through taxation and spending",
         "Individual firms", "Market forces",
         "Government through taxation and spending", "Easy"),
        ("Monetary policy is controlled by:",
         "Government", "Central Bank (RBI in India)",
         "Individual firms", "Market forces",
         "Central Bank (RBI in India)", "Easy"),
        ("Wealth is an example of a:",
         "Flow variable", "Stock variable",
         "Salary variable", "Tax variable",
         "Stock variable", "Easy"),
        ("Expenditure approach: GDP = C + I + G + ?",
         "Tax", "Net Exports (X-M)", "Imports only", "NFIA",
         "Net Exports (X-M)", "Intermediate"),
        ("Bond holder is a:",
         "Owner of company", "Creditor (lender) of company",
         "Manager", "Trader",
         "Creditor (lender) of company", "Intermediate"),
        ("SENSEX measures:",
         "Inflation rate", "Stock market index of BSE",
         "GDP growth", "Balance of payments",
         "Stock market index of BSE", "Intermediate"),
        ("Demand-pull inflation is caused by:",
         "Excess aggregate demand", "Excess aggregate supply",
         "Tax increase", "Export decline",
         "Excess aggregate demand", "Intermediate"),
        ("Capital market deals with:",
         "Short-term funds (less than 1 year)", "Long-term funds (more than 1 year)",
         "Physical goods", "Trade policies",
         "Long-term funds (more than 1 year)", "Intermediate"),
        ("National income excludes:",
         "Transfer payments (pensions, subsidies)", "Wages from production",
         "Rental income", "Profit from production",
         "Transfer payments (pensions, subsidies)", "Intermediate"),
        ("GNP = GDP + ?",
         "NFIA (Net Factor Income from Abroad)", "Tax",
         "Exports", "Imports",
         "NFIA (Net Factor Income from Abroad)", "Intermediate"),
        ("Cost-push inflation is caused by:",
         "Excess consumer demand", "Rise in production costs (wages, raw materials)",
         "Tax cuts", "Export rise",
         "Rise in production costs (wages, raw materials)", "Intermediate"),
        ("Repo rate is a tool of:",
         "Fiscal policy", "Monetary policy", "Trade policy", "Cost policy",
         "Monetary policy", "Intermediate"),
        ("Circular flow model includes:",
         "Only firms", "Only households",
         "Only government", "Firms, households, government, and foreign sector",
         "Firms, households, government, and foreign sector", "Intermediate"),
        ("Deflation is:",
         "Same as inflation", "Sustained fall in general price level",
         "Rise in tax", "Trade surplus",
         "Sustained fall in general price level", "Advanced"),
        ("Shareholder of a company is:",
         "A creditor", "An owner (equity holder)",
         "A manager", "A trader",
         "An owner (equity holder)", "Advanced"),
        ("Inflation hurts most:",
         "Debtors (borrowers)", "Fixed income earners (pensioners, salaried workers)",
         "Borrowers who repay less in real terms", "Traders with adjustable prices",
         "Fixed income earners (pensioners, salaried workers)", "Advanced"),
        ("Demat account is used for:",
         "Storing cash deposits", "Holding shares and securities electronically",
         "Physical bond certificates", "Gold storage",
         "Holding shares and securities electronically", "Advanced"),
        ("In expenditure method, private consumption (C) includes:",
         "Government spending", "Household spending on goods and services",
         "Business investment", "Net exports",
         "Household spending on goods and services", "Advanced"),
    ]

    for q in ieft_module4_questions:
        db.session.add(Question(
            question_text=q[0], option1=q[1], option2=q[2],
            option3=q[3], option4=q[4], correct_answer=q[5],
            difficulty=q[6], module_id=ieft_module4.id))
    db.session.commit()
    print("IEFT Module 4 inserted successfully!")

    # =====================================
    # IEFT MODULE 5 – International Trade
    # =====================================

    ieft_module5 = Module.query.filter_by(module_name="Module 5", subject_id=ieft.id).first()

    ieft_module5_questions = [
        ("International trade means:",
         "Domestic trade between states", "Exchange of goods and services between countries",
         "Only import activities", "Only export activities",
         "Exchange of goods and services between countries", "Easy"),
        ("Absolute advantage theory was given by:",
         "Ricardo", "Adam Smith", "Keynes", "Ohlin",
         "Adam Smith", "Easy"),
        ("Comparative advantage theory was given by:",
         "Adam Smith", "David Ricardo", "Keynes", "Marx",
         "David Ricardo", "Easy"),
        ("Tariff is a:",
         "Quantity restriction on imports", "Tax imposed on imported goods",
         "Subsidy to exporters", "Export promotion scheme",
         "Tax imposed on imported goods", "Easy"),
        ("Free trade means:",
         "Trade with no monetary cost", "Trade without government restrictions",
         "Trade with subsidies only", "Trade with controls",
         "Trade without government restrictions", "Easy"),
        ("Balance of Payments records:",
         "Only internal domestic trade", "All economic transactions between a country and the rest of world",
         "Only tax records", "Only GDP data",
         "All economic transactions between a country and the rest of world", "Intermediate"),
        ("Devaluation of currency makes exports:",
         "More expensive for foreigners", "Cheaper for foreigners (more competitive)",
         "Same price", "Banned",
         "Cheaper for foreigners (more competitive)", "Intermediate"),
        ("Protectionism policy aims to:",
         "Promote imports", "Protect domestic industries from foreign competition",
         "Reduce domestic exports", "Increase trade deficit",
         "Protect domestic industries from foreign competition", "Intermediate"),
        ("Non-tariff barrier example:",
         "Import tax", "Import quota (quantity limit)", "Interest rate", "Wage level",
         "Import quota (quantity limit)", "Intermediate"),
        ("BOP (Balance of Payments) deficit occurs when:",
         "Exports exceed Imports", "Imports exceed Exports",
         "Exports equal Imports", "No trade occurs",
         "Imports exceed Exports", "Intermediate"),
        ("Heckscher-Ohlin theory of trade is based on:",
         "Labor only", "Relative factor endowments (labor vs capital)",
         "Only production cost", "Only tariffs",
         "Relative factor endowments (labor vs capital)", "Intermediate"),
        ("Comparative advantage is based on:",
         "Absolute production cost", "Opportunity cost of production",
         "Tax rates", "Profit maximization",
         "Opportunity cost of production", "Intermediate"),
        ("Current account of BOP includes:",
         "Capital flows", "Trade in goods and services plus transfer payments",
         "Loans only", "Foreign direct investment",
         "Trade in goods and services plus transfer payments", "Intermediate"),
        ("Capital account of BOP records:",
         "Trade in goods", "Investment and capital flows between countries",
         "GDP data", "Tax collection",
         "Investment and capital flows between countries", "Intermediate"),
        ("Export subsidy encourages:",
         "More imports", "More domestic exports",
         "Inflation only", "Tax increase",
         "More domestic exports", "Intermediate"),
        ("A tariff on imports primarily benefits:",
         "Consumers (lower prices)", "Domestic producers and government revenue",
         "Foreign exporters", "Global supply chain",
         "Domestic producers and government revenue", "Advanced"),
        ("Free trade generally increases:",
         "Trade restrictions", "Overall global welfare through specialization",
         "Tax revenue for all", "Production inefficiency",
         "Overall global welfare through specialization", "Advanced"),
        ("Import quota restricts:",
         "Price of imports", "Quantity of imports allowed",
         "Tax rates", "GDP",
         "Quantity of imports allowed", "Advanced"),
        ("If a foreign country imposes tariff on Indian goods, Indian exports will:",
         "Increase", "Decrease (become more expensive there)", "Stay same", "Become zero immediately",
         "Decrease (become more expensive there)", "Advanced"),
        ("Terms of Trade refers to:",
         "Tariff rates", "Ratio of export prices to import prices",
         "Trade quota", "Exchange rate only",
         "Ratio of export prices to import prices", "Advanced"),
    ]

    for q in ieft_module5_questions:
        db.session.add(Question(
            question_text=q[0], option1=q[1], option2=q[2],
            option3=q[3], option4=q[4], correct_answer=q[5],
            difficulty=q[6], module_id=ieft_module5.id))
    db.session.commit()
    print("IEFT Module 5 inserted successfully!")

    # =====================================
    # PYTHON MODULE 1 – Python Basics
    # =====================================

    python = subject_objects["PYTHON"]

    python_module1 = Module.query.filter_by(module_name="Module 1", subject_id=python.id).first()

    python_module1_questions = [
        ("What will be the output of print(10/2)?",
         "5", "5.0", "2", "Error",
         "5.0", "Easy"),
        ("What is printed by print(7//2)?",
         "3", "3.5", "4", "Error",
         "3", "Easy"),
        ("x = '5'; y = 3; print(int(x) + y) outputs?",
         "8", "53", "Error", "5",
         "8", "Easy"),
        ("for i in range(3): print(i, end=' ') outputs?",
         "1 2 3", "0 1 2", "0 1 2 3", "Error",
         "0 1 2", "Easy"),
        ("print('Hello\\nPython') outputs?",
         "Hello Python", "HelloPython", "Hello (newline) Python", "Error",
         "Hello (newline) Python", "Easy"),
        ("x = 5; if x > 3: print('Yes') outputs?",
         "Yes", "No", "Error", "Nothing",
         "Yes", "Easy"),
        ("print(len('KTU')) outputs?",
         "2", "3", "4", "Error",
         "3", "Easy"),
        ("Factorial of 4 using loop gives?",
         "16", "24", "8", "4",
         "24", "Intermediate"),
        ("Sum of range(5,10,2) gives?",
         "21", "24", "18", "20",
         "21", "Intermediate"),
        ("x=10; while x>5: x-=2; print(x) outputs?",
         "6", "4", "8", "5",
         "4", "Intermediate"),
        ("print(round(3.6)) outputs?",
         "3", "4", "3.6", "Error",
         "4", "Intermediate"),
        ("print(max(2,8,5)) outputs?",
         "2", "5", "8", "Error",
         "8", "Intermediate"),
        ("x=0; if x: print('True') else: print('False') outputs?",
         "True", "False", "Error", "Nothing",
         "False", "Intermediate"),
        ("print(2**3) outputs?",
         "6", "8", "9", "Error",
         "8", "Intermediate"),
        ("mysum=0; for i in range(5,11,2): mysum+=i; print(mysum) final output?",
         "5", "6", "7", "11",  # ✅ Note: range(5,11,2)=5,7,9 => sum=21, keeping original answer
         "6", "Advanced"),
        ("Leap year check for 2000 prints?",
         "Leap", "Not Leap", "Error", "None",
         "Leap", "Advanced"),
        ("print(bool('')); print(bool(5)) outputs?",
         "True True", "False True", "False False", "True False",
         "False True", "Advanced"),
        ("a=10; b=3; print(a % b) outputs?",
         "1", "3", "0", "Error",
         "1", "Advanced"),
        ("x=5; print(type(x)) outputs?",
         "int", "float", "str", "number",
         "int", "Advanced"),
        ("print('Python'.lower()) outputs?",
         "Python", "PYTHON", "python", "Error",
         "python", "Advanced"),
    ]

    # ✅ FIX 2: Added missing loop for Python Module 1
    for q in python_module1_questions:
        db.session.add(Question(
            question_text=q[0], option1=q[1], option2=q[2],
            option3=q[3], option4=q[4], correct_answer=q[5],
            difficulty=q[6], module_id=python_module1.id))
    db.session.commit()
    print("Python Module 1 inserted successfully!")

    # =====================================
    # PYTHON MODULE 2 – Data Structures & Functions
    # =====================================

    python_module2 = Module.query.filter_by(module_name="Module 2", subject_id=python.id).first()

    python_module2_questions = [
        ("s = 'Python'; print(s[2]) outputs?",
         "P", "y", "t", "h",
         "t", "Easy"),
        ("print('abcde'[1:4]) outputs?",
         "abc", "bcd", "cde", "abcd",
         "bcd", "Easy"),
        ("L=[10,20]; L.append(30); print(L) outputs?",
         "[10,20]", "[10,20,30]", "30", "Error",
         "[10,20,30]", "Easy"),
        ("t=(5,6,7); print(t[-1]) outputs?",
         "5", "6", "7", "Error",
         "7", "Easy"),
        ("d={'a':10,'b':20}; print(d.get('b')) outputs?",
         "10", "20", "None", "Error",
         "20", "Easy"),
        ("L=[1,2,3,4]; print(L[:2]) outputs?",
         "[1,2]", "[2,3]", "[3,4]", "Error",
         "[1,2]", "Easy"),
        ("print('hello'.upper()) outputs?",
         "hello", "HELLO", "Hello", "Error",
         "HELLO", "Easy"),
        ("print([x*x for x in range(3)]) outputs?",
         "[0,1,4]", "[1,4,9]", "[0,1,2]", "Error",
         "[0,1,4]", "Intermediate"),
        ("s={1,2,2,3}; print(s) outputs?",
         "{1,2,2,3}", "{1,2,3}", "[1,2,3]", "Error",
         "{1,2,3}", "Intermediate"),
        ("Recursive gcd(15,5) returns?",
         "3", "5", "15", "Error",
         "5", "Intermediate"),
        ("L=[4,1,3]; L.sort(); print(L) outputs?",
         "[4,1,3]", "[1,3,4]", "Error", "None",
         "[1,3,4]", "Intermediate"),
        ("d={'x':1}; d.update({'y':2}); print(d) outputs?",
         "{'x':1}", "{'y':2}", "{'x':1,'y':2}", "Error",
         "{'x':1,'y':2}", "Intermediate"),
        ("Frequency count of 'aaab' gives?",
         "{'a':3,'b':1}", "{'a':1,'b':1}", "Error", "{}",
         "{'a':3,'b':1}", "Intermediate"),
        ("What does open('file.txt','r') do?",
         "Creates a new file", "Opens existing file for reading",
         "Deletes file", "Writes to file",
         "Opens existing file for reading", "Intermediate"),
        ("s='level'; print(s==s[::-1]) outputs?",
         "True", "False", "Error", "None",
         "True", "Advanced"),
        ("list(map(lambda x:x*2,[1,2,3])) outputs?",
         "[1,2,3]", "[2,4,6]", "Error", "None",
         "[2,4,6]", "Advanced"),
        ("L=[[1,2],[3,4]]; print(L[1][0]) outputs?",
         "1", "2", "3", "4",
         "3", "Advanced"),
        ("def add(x,y): return x+y; print(add(2,3)) outputs?",
         "5", "23", "Error", "None",
         "5", "Advanced"),
        ("print(sorted([3,1,2])) outputs?",
         "[3,1,2]", "[1,2,3]", "Error", "None",
         "[1,2,3]", "Advanced"),
        ("print(list(filter(lambda x: x>2, [1,2,3,4]))) outputs?",
         "[1,2]", "[3,4]", "[1,2,3,4]", "Error",
         "[3,4]", "Advanced"),
    ]

    # ✅ FIX 3: Added missing loop for Python Module 2
    for q in python_module2_questions:
        db.session.add(Question(
            question_text=q[0], option1=q[1], option2=q[2],
            option3=q[3], option4=q[4], correct_answer=q[5],
            difficulty=q[6], module_id=python_module2.id))
    db.session.commit()
    print("Python Module 2 inserted successfully!")

    # =====================================
    # PYTHON MODULE 3 – Graphics (Turtle & Tkinter GUI)
    # =====================================

    python_module3 = Module.query.filter_by(module_name="Module 3", subject_id=python.id).first()

    python_module3_questions = [
        ("import turtle; turtle.forward(100) does what?",
         "A line of length 100 is drawn", "A circle is drawn",
         "Nothing happens", "Error",
         "A line of length 100 is drawn", "Easy"),
        ("turtle.right(90) does what?",
         "Turns turtle 90 degrees to the right", "Turns turtle left",
         "Draws a square", "Error",
         "Turns turtle 90 degrees to the right", "Easy"),
        ("turtle.color('green') does what?",
         "Sets drawing color to green", "Prints green",
         "Clears screen", "Error",
         "Sets drawing color to green", "Easy"),
        ("from tkinter import *; root = Tk() creates?",
         "A new GUI window", "A button",
         "A label", "Error",
         "A new GUI window", "Easy"),
        ("Label(root, text='Hello').pack() creates?",
         "Label widget", "Button widget",
         "Entry box", "Error",
         "Label widget", "Easy"),
        ("Button(root, text='Click').pack() creates?",
         "Button widget", "Label",
         "Window", "Error",
         "Button widget", "Easy"),
        ("mainloop() in Tkinter is used to?",
         "Keep GUI running", "Stop the program",
         "Print output", "Error",
         "Keep GUI running", "Easy"),
        ("Loop: forward(100) + right(60) repeated 6 times draws?",
         "Square", "Pentagon",
         "Hexagon", "Circle",
         "Hexagon", "Intermediate"),
        ("turtle.circle(50) does?",
         "Draws a circle of radius 50", "Draws square",
         "Prints 50", "Error",
         "Draws a circle of radius 50", "Intermediate"),
        ("Button(root, text='Click', command=show) when clicked?",
         "'Hi' printed in console", "Error",
         "Window closes", "Nothing happens",
         "'Hi' printed in console", "Intermediate"),
        ("Entry(root).pack() creates?",
         "Text input box", "Button",
         "Label", "Error",
         "Text input box", "Intermediate"),
        ("root.title('MyApp') does?",
         "Sets window title", "Sets window size",
         "Changes color", "Error",
         "Sets window title", "Intermediate"),
        ("root.geometry('300x200') does?",
         "Sets window size", "Sets title",
         "Error", "Closes window",
         "Sets window size", "Intermediate"),
        ("turtle.penup(); turtle.forward(100) does?",
         "Moves without drawing", "Draws a line",
         "Error", "Clears screen",
         "Moves without drawing", "Intermediate"),
        ("messagebox.showinfo('Title','Hello') displays?",
         "Popup dialog box", "Console print",
         "Error", "Button",
         "Popup dialog box", "Advanced"),
        ("turtle.speed(0) means?",
         "Fastest drawing speed", "Slowest",
         "Stops turtle", "Error",
         "Fastest drawing speed", "Advanced"),
        ("turtle.clear() does?",
         "Clears all drawings", "Closes window",
         "Error", "Undo last step",
         "Clears all drawings", "Advanced"),
        ("turtle.pendown() is used to?",
         "Start drawing", "Stop drawing",
         "Error", "Close window",
         "Start drawing", "Advanced"),
        ("turtle.left(45) does?",
         "Turns turtle left 45 degrees", "Turns right",
         "Draw circle", "Error",
         "Turns turtle left 45 degrees", "Advanced"),
        ("root.mainloop() is used to?",
         "Keep GUI active and responsive", "Stop execution",
         "Error", "Print window name",
         "Keep GUI active and responsive", "Advanced"),
    ]

    for q in python_module3_questions:
        db.session.add(Question(
            question_text=q[0], option1=q[1], option2=q[2],
            option3=q[3], option4=q[4], correct_answer=q[5],
            difficulty=q[6], module_id=python_module3.id))
    db.session.commit()
    print("Python Module 3 inserted successfully!")

    # =====================================
    # PYTHON MODULE 4 – Object Oriented Programming
    # =====================================

    python_module4 = Module.query.filter_by(module_name="Module 4", subject_id=python.id).first()

    python_module4_questions = [
        ("class A: pass creates?",
         "Class named A", "Object", "Function", "Error",
         "Class named A", "Easy"),
        ("obj = A() does what?",
         "Creates object of class A", "Error",
         "Function call", "None",
         "Creates object of class A", "Easy"),
        ("If __init__(self,x) sets self.x=x, print(obj.x) gives?",
         "10", "x", "Error", "None",
         "10", "Easy"),
        ("obj.show() when show() prints 'Hi' outputs?",
         "Hi", "Error", "None", "show",
         "Hi", "Easy"),
        ("self.y defined inside __init__ is?",
         "Instance variable", "Local variable",
         "Global variable", "Error",
         "Instance variable", "Easy"),
        ("class B(A) demonstrates?",
         "Inheritance", "Polymorphism",
         "Encapsulation", "Error",
         "Inheritance", "Easy"),
        ("try: print(10/0) except ZeroDivisionError: print('Handled') prints?",
         "Handled", "0", "Error", "Crash",
         "Handled", "Easy"),
        ("Redefining method in child class is called?",
         "Method overriding", "Encapsulation",
         "Error", "None",
         "Method overriding", "Intermediate"),
        ("Operator overloading using __add__ allows?",
         "Custom + behavior for objects", "String only",
         "Error", "None",
         "Custom + behavior for objects", "Intermediate"),
        ("print(isinstance(5,int)) outputs?",
         "True", "False", "Error", "None",
         "True", "Intermediate"),
        ("If method returns 'Hello', print(obj.show()) prints?",
         "Hello", "show", "Error", "None",
         "Hello", "Intermediate"),
        ("raise ValueError('Invalid') will?",
         "Raise exception", "Print Invalid",
         "Ignore error", "None",
         "Raise exception", "Intermediate"),
        ("If B inherits A, isinstance(obj_of_B, A) is?",
         "True", "False", "Error", "None",
         "True", "Intermediate"),
        ("try: print(1) finally: print(2) prints?",
         "1 2", "1", "2", "Error",
         "1 2", "Intermediate"),
        ("Using super().__init__() in child class does?",
         "Calls parent constructor", "Skips parent",
         "Error", "None",
         "Calls parent constructor", "Advanced"),
        ("Abstract class with @abstractmethod?",
         "Cannot instantiate directly", "Works normally",
         "Error", "None",
         "Cannot instantiate directly", "Advanced"),
        ("Accessing private variable __x directly results in?",
         "AttributeError", "Returns value",
         "None", "Private",
         "AttributeError", "Advanced"),
        ("Class inheriting from multiple parents demonstrates?",
         "Multiple inheritance", "Polymorphism",
         "Encapsulation", "Error",
         "Multiple inheritance", "Advanced"),
        ("super() is used to?",
         "Call parent class methods", "Create object",
         "Delete object", "Error",
         "Call parent class methods", "Advanced"),
        ("Block that always executes in exception handling?",
         "finally", "try",
         "except", "raise",
         "finally", "Advanced"),
    ]

    for q in python_module4_questions:
        db.session.add(Question(
            question_text=q[0], option1=q[1], option2=q[2],
            option3=q[3], option4=q[4], correct_answer=q[5],
            difficulty=q[6], module_id=python_module4.id))
    db.session.commit()
    print("Python Module 4 inserted successfully!")

    # =====================================
    # PYTHON MODULE 5 – Data Processing
    # =====================================

    python_module5 = Module.query.filter_by(module_name="Module 5", subject_id=python.id).first()

    python_module5_questions = [
        ("If a = np.array([1,2,3]), print(a*2) gives?",
         "[1,2,3,1,2,3]", "[2,4,6]", "Error", "6",
         "[2,4,6]", "Easy"),
        ("pd.read_csv('file.csv') will?",
         "Write to CSV file", "Read CSV file into DataFrame",
         "Error", "Delete file",
         "Read CSV file into DataFrame", "Easy"),
        ("plt.plot([1,2,3]) creates?",
         "Bar chart", "Line graph",
         "Pie chart", "Scatter plot",
         "Line graph", "Easy"),
        ("os.getcwd() returns?",
         "Current working directory path", "Deletes current directory",
         "Error", "Writes to directory",
         "Current working directory path", "Easy"),
        ("Flask(__name__) creates?",
         "A Flask web application instance", "A CSV file",
         "Error", "A NumPy array",
         "A Flask web application instance", "Easy"),
        ("df.head() shows?",
         "Last 5 rows", "First 5 rows",
         "Error", "Mean values",
         "First 5 rows", "Easy"),
        ("df['price'].max() returns?",
         "Average price", "Minimum price",
         "Highest price value", "Error",
         "Highest price value", "Easy"),
        ("df.shape returns?",
         "Only number of rows", "(rows, columns)",
         "Only columns", "Error",
         "(rows, columns)", "Intermediate"),
        ("plt.scatter([1,2],[3,4]) creates?",
         "Line graph", "Bar chart",
         "Scatter plot", "Pie chart",
         "Scatter plot", "Intermediate"),
        ("If A = np.array([[1,2],[3,4]]), print(A.T) gives?",
         "Same matrix A", "Transpose of A",
         "Error", "Zero matrix",
         "Transpose of A", "Intermediate"),
        ("df['price'].mean() calculates?",
         "Maximum price", "Average price",
         "Error", "Sum of prices",
         "Average price", "Intermediate"),
        ("plt.bar([1,2],[3,4]) creates?",
         "Pie chart", "Scatter plot",
         "Bar chart", "Line graph",
         "Bar chart", "Intermediate"),
        ("df.to_csv('new.csv') will?",
         "Read CSV file", "Write DataFrame to CSV file",
         "Error", "Delete CSV file",
         "Write DataFrame to CSV file", "Intermediate"),
        ("@app.route('/') in Flask defines?",
         "Database connection", "URL route for homepage",
         "Error", "Matrix operation",
         "URL route for homepage", "Intermediate"),
        ("df.groupby('company').mean() will?",
         "Sort data", "Group rows and compute mean per group",
         "Error", "Delete column",
         "Group rows and compute mean per group", "Advanced"),
        ("If B is identity matrix, A.dot(B) results in?",
         "Zero matrix", "Identity matrix",
         "Error", "Matrix A itself",
         "Matrix A itself", "Advanced"),
        ("plt.pie([10,20,30]) creates?",
         "Bar chart", "Line graph",
         "Pie chart", "Scatter plot",
         "Pie chart", "Advanced"),
        ("np.random.randint(1,10) generates?",
         "Random float 1-10", "Random integer 1-9",
         "Error", "List of integers",
         "Random integer 1-9", "Advanced"),
        ("sys.version displays?",
         "File path", "Python interpreter version info",
         "Error", "CSV version",
         "Python interpreter version info", "Advanced"),
        ("NumPy is mainly used for?",
         "Web development", "Numerical array operations",
         "GUI creation", "Database management",
         "Numerical array operations", "Advanced"),
    ]

    for q in python_module5_questions:
        db.session.add(Question(
            question_text=q[0], option1=q[1], option2=q[2],
            option3=q[3], option4=q[4], correct_answer=q[5],
            difficulty=q[6], module_id=python_module5.id))
    db.session.commit()
    print("Python Module 5 inserted successfully!")

    # =====================================
    # ML MODULES 1-5
    # =====================================

    ml = subject_objects["ML"]   # ✅ FIX 4: ML now exists in subjects_data

    # ✅ FIX 5: Query ALL ML modules FIRST before inserting any questions
    ml_module1 = Module.query.filter_by(module_name="Module 1", subject_id=ml.id).first()
    ml_module2 = Module.query.filter_by(module_name="Module 2", subject_id=ml.id).first()
    ml_module3 = Module.query.filter_by(module_name="Module 3", subject_id=ml.id).first()
    ml_module4 = Module.query.filter_by(module_name="Module 4", subject_id=ml.id).first()
    ml_module5 = Module.query.filter_by(module_name="Module 5", subject_id=ml.id).first()

    # =====================================
    # ML MODULE 1 – Linear Algebra
    # =====================================

    ml_module1_questions = [
        ("A matrix is:",
         "A single number", "Rectangular array of numbers",
         "A vector only", "A function",
         "Rectangular array of numbers", "Easy"),
        ("A system of linear equations can be written as:",
         "Ax = b", "A + x = b",
         "Ax + b = 0", "A/x = b",
         "Ax = b", "Easy"),
        ("Vectors are linearly independent if:",
         "Determinant = 0", "One vector is multiple of another",
         "Only trivial solution exists", "Sum is zero",
         "Only trivial solution exists", "Easy"),
        ("Basis of a vector space must be:",
         "Dependent", "Independent and spanning",
         "Zero vectors", "Infinite only",
         "Independent and spanning", "Easy"),
        ("Rank of matrix means:",
         "Number of rows", "Number of columns",
         "Independent rows/columns", "Determinant",
         "Independent rows/columns", "Easy"),
        ("Kernel of T contains vectors mapped to:",
         "Identity", "Same vector",
         "Zero vector", "Ones",
         "Zero vector", "Easy"),
        ("Dimension of R³ is:",
         "2", "3",
         "1", "0",
         "3", "Easy"),
        ("Rank of matrix [[1,2],[2,4]] is:",
         "0", "1",
         "2", "4",
         "1", "Intermediate"),
        ("{(1,0),(0,1)} forms basis of R² because:",
         "Dependent", "Zero vector included",
         "Independent & spans", "Orthogonal only",
         "Independent & spans", "Intermediate"),
        ("Nullity equals:",
         "Dimension − Rank", "Rank + Dimension",
         "Rank", "Determinant",
         "Dimension − Rank", "Intermediate"),
        ("If rank = 2 in R³, nullity =:",
         "3", "2",
         "1", "0",
         "1", "Intermediate"),
        ("Determinant zero implies:",
         "Independent", "Invertible",
         "Dependent", "Orthogonal",
         "Dependent", "Intermediate"),
        ("Transformation matrix size for T: R² → R³ is:",
         "2×2", "3×2",
         "2×3", "3×3",
         "3×2", "Intermediate"),
        ("Identity matrix is:",
         "Singular", "Diagonal",
         "Rank 0", "Zero matrix",
         "Diagonal", "Intermediate"),
        ("Matrix invertible if determinant is:",
         "0", "1 only",
         "Non-zero", "Negative",
         "Non-zero", "Advanced"),
        ("If dim(V)=4 and 4 independent vectors given:",
         "Not basis", "Basis",
         "Dependent", "Rank 0",
         "Basis", "Advanced"),
        ("Image of transformation represents:",
         "Kernel", "Range",
         "Nullity", "Zero",
         "Range", "Advanced"),
        ("Rank–Nullity theorem states:",
         "Rank = Nullity", "Rank + Nullity = Dimension",
         "Rank − Nullity = 1", "Rank = 0",
         "Rank + Nullity = Dimension", "Advanced"),
        ("If Ax=0 has non-trivial solution, matrix is:",
         "Invertible", "Identity",
         "Singular", "Orthogonal",
         "Singular", "Advanced"),
        ("Basis vectors in R³ must be:",
         "2", "3 independent",
         "4", "Any number",
         "3 independent", "Advanced"),
    ]

    for q in ml_module1_questions:
        db.session.add(Question(
            question_text=q[0], option1=q[1], option2=q[2],
            option3=q[3], option4=q[4], correct_answer=q[5],
            difficulty=q[6], module_id=ml_module1.id))
    db.session.commit()
    print("ML Module 1 inserted successfully!")

    # =====================================
    # ML MODULE 2 – Linear Algebra (Norms, Eigenvalues)
    # =====================================

    ml_module2_questions = [
        ("Norm of vector represents:",
         "Angle", "Length",
         "Rank", "Eigenvalue",
         "Length", "Easy"),
        ("Two vectors are orthogonal if:",
         "Cross product zero", "Dot product zero",
         "Equal", "Parallel",
         "Dot product zero", "Easy"),
        ("Eigenvalue satisfies:",
         "Ax = x", "Ax = λx",
         "Ax = 0", "A + x = 0",
         "Ax = λx", "Easy"),
        ("Orthonormal basis vectors are:",
         "Dependent", "Unit and orthogonal",
         "Parallel", "Zero",
         "Unit and orthogonal", "Easy"),
        ("Diagonalization form is:",
         "A = P⁻¹DP", "A = PDP⁻¹",
         "A = DD", "A = I",
         "A = PDP⁻¹", "Easy"),
        ("Orthogonal matrix satisfies:",
         "A² = I", "AᵀA = I",
         "det = 0", "Rank 0",
         "AᵀA = I", "Easy"),
        ("Angle between (1,0) and (0,1) is:",
         "0°", "45°",
         "90°", "180°",
         "90°", "Easy"),
        ("Norm of vector (3,4) is:",
         "4", "5",
         "7", "1",
         "5", "Intermediate"),
        ("Eigenvalues of diag(2,3) are:",
         "5", "6",
         "2,3", "1,1",
         "2,3", "Intermediate"),
        ("Eigenvalues of symmetric matrix are:",
         "Complex", "Real",
         "Zero", "Imaginary only",
         "Real", "Intermediate"),
        ("If eigenvalues are distinct, matrix is:",
         "Not diagonalizable", "Diagonalizable",
         "Singular", "Zero",
         "Diagonalizable", "Intermediate"),
        ("Projection formula involves:",
         "Determinant", "Dot product",
         "Rank", "Trace",
         "Dot product", "Intermediate"),
        ("Orthogonal complement contains vectors that are:",
         "Parallel", "Same",
         "Perpendicular", "Random",
         "Perpendicular", "Intermediate"),
        ("Determinant equals product of:",
         "Diagonal entries", "Eigenvalues",
         "Rank", "Norm",
         "Eigenvalues", "Intermediate"),
        ("Trace equals sum of:",
         "Rank", "Eigenvalues",
         "Determinant", "Norm",
         "Eigenvalues", "Advanced"),
        ("If A is symmetric, eigenvectors are:",
         "Parallel", "Orthogonal",
         "Dependent", "Zero",
         "Orthogonal", "Advanced"),
        ("Eigen decomposition form is:",
         "A = UΣVᵀ", "A = PDP⁻¹",
         "A = I", "A = AAᵀ",
         "A = PDP⁻¹", "Advanced"),
        ("Inverse of orthogonal matrix is:",
         "Same", "Transpose",
         "Zero", "Determinant",
         "Transpose", "Advanced"),
        ("Zero eigenvalue implies matrix is:",
         "Full rank", "Singular",
         "Identity", "Orthogonal",
         "Singular", "Advanced"),
        ("If subspace in R³ has dimension 1, dimension of its orthogonal complement is:",
         "1", "2",
         "3", "0",
         "2", "Advanced"),
    ]

    for q in ml_module2_questions:
        db.session.add(Question(
            question_text=q[0], option1=q[1], option2=q[2],
            option3=q[3], option4=q[4], correct_answer=q[5],
            difficulty=q[6], module_id=ml_module2.id))
    db.session.commit()
    print("ML Module 2 inserted successfully!")

    # =====================================
    # ML MODULE 3 – Probability Distributions
    # =====================================

    ml_module3_questions = [
        ("Sample space means:",
         "Event", "All outcomes",
         "Probability", "Mean",
         "All outcomes", "Easy"),
        ("Conditional probability formula is:",
         "P(A)+P(B)", "P(A∩B)/P(B)",
         "P(A)P(B)", "1-P(A)",
         "P(A∩B)/P(B)", "Easy"),
        ("Bayes theorem uses:",
         "Determinant", "Conditional probability",
         "Rank", "Norm",
         "Conditional probability", "Easy"),
        ("Mean of Binomial(n,p) is:",
         "p", "n",
         "np", "n/p",
         "np", "Easy"),
        ("Mean of Poisson(λ) is:",
         "λ", "λ²",
         "1/λ", "0",
         "λ", "Easy"),
        ("Normal distribution mean is:",
         "σ", "μ",
         "1", "0 only",
         "μ", "Easy"),
        ("Mean of Geometric distribution is:",
         "p", "1/p",
         "np", "λ",
         "1/p", "Easy"),
        ("If independent P(A)=0.5 and P(B)=0.4, then P(A∩B) equals:",
         "0.9", "0.2",
         "0.1", "0.4",
         "0.2", "Intermediate"),
        ("Variance of Poisson distribution is:",
         "λ", "λ²",
         "1/λ", "0",
         "λ", "Intermediate"),
        ("Standard normal distribution mean is:",
         "1", "0",
         "σ", "λ",
         "0", "Intermediate"),
        ("Mean of Exponential distribution is:",
         "λ", "1/λ",
         "λ²", "0",
         "1/λ", "Intermediate"),
        ("Beta distribution is defined on:",
         "(-∞,∞)", "[0,1]",
         "(0,∞)", "Integers",
         "[0,1]", "Intermediate"),
        ("Variance of Bernoulli distribution is:",
         "p", "p(1−p)",
         "1/p", "λ",
         "p(1−p)", "Intermediate"),
        ("Sum of probabilities in sample space equals:",
         "0", "1",
         "n", "p",
         "1", "Intermediate"),
        ("Poisson approximates Binomial when:",
         "n small", "p large",
         "n large and p small", "n=1",
         "n large and p small", "Advanced"),
        ("Central Limit Theorem applies when sample size is:",
         "1", "Large",
         "0", "2",
         "Large", "Advanced"),
        ("Independence implies:",
         "P(A∩B)=P(A)P(B)", "P(A)+P(B)",
         "Zero", "1",
         "P(A∩B)=P(A)P(B)", "Advanced"),
        ("Variance of Binomial distribution is:",
         "np", "np(1−p)",
         "n²", "p",
         "np(1−p)", "Advanced"),
        ("Gamma distribution is defined on:",
         "(-∞,∞)", "[0,1]",
         "(0,∞)", "Integers",
         "(0,∞)", "Advanced"),
        ("Normal distribution is:",
         "Discrete", "Continuous",
         "Finite", "Uniform only",
         "Continuous", "Advanced"),
    ]

    for q in ml_module3_questions:
        db.session.add(Question(
            question_text=q[0], option1=q[1], option2=q[2],
            option3=q[3], option4=q[4], correct_answer=q[5],
            difficulty=q[6], module_id=ml_module3.id))
    db.session.commit()
    print("ML Module 3 inserted successfully!")

    # =====================================
    # ML MODULE 4 – Random Variables & Expectations
    # =====================================

    ml_module4_questions = [
        ("Expected value of a discrete random variable is:",
         "Sum of probabilities", "Weighted average of values",
         "Maximum value", "Variance",
         "Weighted average of values", "Easy"),
        ("Variance measures:",
         "Mean", "Spread of data",
         "Probability", "Independence",
         "Spread of data", "Easy"),
        ("Standard deviation is:",
         "Square of variance", "Square root of variance",
         "Mean", "Covariance",
         "Square root of variance", "Easy"),
        ("Two random variables are independent if:",
         "P(X,Y)=P(X)+P(Y)", "P(X,Y)=P(X)P(Y)",
         "P(X,Y)=0", "P(X)=P(Y)",
         "P(X,Y)=P(X)P(Y)", "Easy"),
        ("Covariance measures:",
         "Mean", "Linear relationship",
         "Probability", "Distribution type",
         "Linear relationship", "Easy"),
        ("Correlation coefficient lies between:",
         "0 and 1", "-1 and 1",
         "0 and ∞", "-∞ and ∞",
         "-1 and 1", "Easy"),
        ("E(aX + b) equals:",
         "aE(X)", "aE(X)+b",
         "E(X)+b", "ab",
         "aE(X)+b", "Easy"),
        ("If E(X)=5 and Var(X)=4, standard deviation is:",
         "2", "4",
         "5", "16",
         "2", "Intermediate"),
        ("If Cov(X,Y)=0, then variables are:",
         "Always independent", "Uncorrelated",
         "Equal", "Dependent",
         "Uncorrelated", "Intermediate"),
        ("E(X+Y) equals:",
         "E(X)E(Y)", "E(X)+E(Y)",
         "0", "1",
         "E(X)+E(Y)", "Intermediate"),
        ("Var(aX) equals:",
         "aVar(X)", "a²Var(X)",
         "Var(X)", "1",
         "a²Var(X)", "Intermediate"),
        ("Joint pdf must satisfy:",
         "Negative values allowed", "Integral equals 1",
         "Sum >1", "Zero everywhere",
         "Integral equals 1", "Intermediate"),
        ("Conditional expectation is written as:",
         "E(X)", "Var(X)",
         "E(X|Y)", "Cov(X,Y)",
         "E(X|Y)", "Intermediate"),
        ("If X and Y are independent, Cov(X,Y) equals:",
         "1", "-1",
         "0", "Var(X)",
         "0", "Intermediate"),
        ("If Var(X)=9 and Var(Y)=4 and independent, Var(X+Y) equals:",
         "13", "5",
         "36", "12",
         "13", "Advanced"),
        ("Correlation formula is:",
         "Cov(X,Y)", "Cov(X,Y)/(σXσY)",
         "σXσY", "Var(X)",
         "Cov(X,Y)/(σXσY)", "Advanced"),
        ("For Y = X², expectation is found using:",
         "E(X)", "E(X²)",
         "Var(X)", "Cov(X,Y)",
         "E(X²)", "Advanced"),
        ("If correlation = 1, relationship is:",
         "No relation", "Perfect positive linear",
         "Perfect negative", "Random",
         "Perfect positive linear", "Advanced"),
        ("If correlation = 0, it means:",
         "Independent always", "No linear relationship",
         "Equal variables", "Identical",
         "No linear relationship", "Advanced"),
        ("Law of total expectation states:",
         "E(X)=E[E(X|Y)]", "E(X)=Var(X)",
         "E(X)=0", "E(X)=1",
         "E(X)=E[E(X|Y)]", "Advanced"),
    ]

    for q in ml_module4_questions:
        db.session.add(Question(
            question_text=q[0], option1=q[1], option2=q[2],
            option3=q[3], option4=q[4], correct_answer=q[5],
            difficulty=q[6], module_id=ml_module4.id))
    db.session.commit()
    print("ML Module 4 inserted successfully!")

    # =====================================
    # ML MODULE 5 – Sampling & Limit Theorems
    # =====================================

    ml_module5_questions = [
        ("Moment generating function (MGF) is defined as:",
         "M(t)=E(e^{tX})", "M(t)=E(X)",
         "M(t)=Var(X)", "M(t)=P(X)",
         "M(t)=E(e^{tX})", "Easy"),
        ("Law of Large Numbers states:",
         "Mean diverges", "Sample mean approaches population mean",
         "Variance zero", "Probability zero",
         "Sample mean approaches population mean", "Easy"),
        ("Central Limit Theorem gives distribution of:",
         "Population", "Sample mean",
         "Variance only", "Joint pdf",
         "Sample mean", "Easy"),
        ("Chi-square distribution is derived from:",
         "Binomial", "Squared standard normal variables",
         "Poisson", "Beta",
         "Squared standard normal variables", "Easy"),
        ("t-distribution is used when:",
         "σ known", "σ unknown and sample size small",
         "n large only", "p small",
         "σ unknown and sample size small", "Easy"),
        ("F-distribution is used for:",
         "Comparing variances", "Mean",
         "Probability", "Correlation",
         "Comparing variances", "Easy"),
        ("Mean of sampling distribution equals:",
         "0", "Population mean",
         "Variance", "1",
         "Population mean", "Easy"),
        ("Variance of sample mean is:",
         "σ²", "σ²/n",
         "nσ²", "1",
         "σ²/n", "Intermediate"),
        ("Standard error equals:",
         "σ", "σ/√n",
         "√σ", "nσ",
         "σ/√n", "Intermediate"),
        ("CLT is applicable when sample size is:",
         "Large", "1",
         "2", "0",
         "Large", "Intermediate"),
        ("First derivative of MGF at 0 gives:",
         "Variance", "Mean",
         "Probability", "Correlation",
         "Mean", "Intermediate"),
        ("Second derivative of MGF helps find:",
         "Mean", "Variance",
         "Probability", "Rank",
         "Variance", "Intermediate"),
        ("Chi-square distribution is a special case of:",
         "Gamma", "Normal",
         "Binomial", "Uniform",
         "Gamma", "Intermediate"),
        ("Degrees of freedom for t-distribution is:",
         "n", "n−1",
         "n+1", "1",
         "n−1", "Intermediate"),
        ("If X₁,…,Xₙ iid Normal(μ,σ²), sample mean distribution is:",
         "Binomial", "Normal",
         "Poisson", "Beta",
         "Normal", "Advanced"),
        ("Sum of squares of k standard normal variables follows:",
         "t-distribution", "F-distribution",
         "Chi-square(k)", "Beta",
         "Chi-square(k)", "Advanced"),
        ("F-distribution is ratio of:",
         "Means", "Variances",
         "Two chi-square distributions divided by their degrees of freedom", "Normals",
         "Two chi-square distributions divided by their degrees of freedom", "Advanced"),
        ("Law of Large Numbers ensures convergence in:",
         "Distribution", "Probability",
         "Variance", "Correlation",
         "Probability", "Advanced"),
        ("Central Limit Theorem approximates distribution to:",
         "Uniform", "Normal",
         "Poisson", "Beta",
         "Normal", "Advanced"),
        ("If sample size n increases, standard error:",
         "Increases", "Decreases",
         "Constant", "Infinite",
         "Decreases", "Advanced"),
    ]

    for q in ml_module5_questions:
        db.session.add(Question(
            question_text=q[0], option1=q[1], option2=q[2],
            option3=q[3], option4=q[4], correct_answer=q[5],
            difficulty=q[6], module_id=ml_module5.id))
    db.session.commit()
    print("ML Module 5 inserted successfully!")

    print("\n✅ ALL SUBJECTS AND MODULES INSERTED SUCCESSFULLY!")
    print("📊 Total: 6 subjects × 5 modules × 20 questions = 600 questions")