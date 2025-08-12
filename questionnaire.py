# questionnaire.py
import streamlit as st

questions = {
    'RIASEC': {
        'Realistic': [
            ("How much do you enjoy working with tools and machines?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How comfortable are you with physical, hands-on work?", [
                "Very uncomfortable", "Somewhat uncomfortable", "Neutral", "Comfortable", "Very comfortable"]),
            ("How interested are you in building or repairing things?", [
                "Not interested", "Slightly interested", "Moderately interested", "Very interested", "Extremely interested"]),
            ("How much do you enjoy outdoor activities and working in nature?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How confident are you in your ability to work with your hands?", [
                "Not confident", "Slightly confident", "Moderately confident", "Very confident", "Extremely confident"]),
            ("How interested are you in operating vehicles, machinery, or equipment?", [
                "Not interested", "Slightly interested", "Moderately interested", "Very interested", "Extremely interested"]),
            ("How much do you enjoy solving practical, hands-on problems?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How comfortable are you with physically demanding work?", [
                "Very uncomfortable", "Somewhat uncomfortable", "Neutral", "Comfortable", "Very comfortable"]),
            ("How interested are you in working with plants, animals, or materials like wood, tools, or machinery?", [
                "Not interested", "Slightly interested", "Moderately interested", "Very interested", "Extremely interested"]),
            ("How much do you value practical skills over abstract thinking?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"])
        ],
        'Investigative': [
            ("How much do you enjoy solving complex problems?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How interested are you in conducting research?", [
                "Not interested", "Slightly interested", "Moderately interested", "Very interested", "Extremely interested"]),
            ("How comfortable are you with analyzing data and information?", [
                "Very uncomfortable", "Somewhat uncomfortable", "Neutral", "Comfortable", "Very comfortable"]),
            ("How much do you enjoy learning about scientific theories?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How interested are you in exploring new ideas and concepts?", [
                "Not interested", "Slightly interested", "Moderately interested", "Very interested", "Extremely interested"]),
            ("How much do you enjoy working independently on intellectual tasks?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How comfortable are you with using logic to solve problems?", [
                "Very uncomfortable", "Somewhat uncomfortable", "Neutral", "Comfortable", "Very comfortable"]),
            ("How interested are you in conducting experiments or studies?", [
                "Not interested", "Slightly interested", "Moderately interested", "Very interested", "Extremely interested"]),
            ("How much do you enjoy reading scientific or technical materials?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How confident are you in your ability to understand complex theories?", [
                "Not confident", "Slightly confident", "Moderately confident", "Very confident", "Extremely confident"])
        ],
        'Artistic': [
            ("How much do you enjoy expressing yourself creatively?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How interested are you in visual arts (painting, drawing, sculpture, etc.)?", [
                "Not interested", "Slightly interested", "Moderately interested", "Very interested", "Extremely interested"]),
            ("How comfortable are you with thinking outside the box?", [
                "Very uncomfortable", "Somewhat uncomfortable", "Neutral", "Comfortable", "Very comfortable"]),
            ("How much do you enjoy writing creatively?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How interested are you in performing arts (music, dance, theater)?", [
                "Not interested", "Slightly interested", "Moderately interested", "Very interested", "Extremely interested"]),
            ("How much do you value originality and self-expression?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How comfortable are you with ambiguity and lack of structure?", [
                "Very uncomfortable", "Somewhat uncomfortable", "Neutral", "Comfortable", "Very comfortable"]),
            ("How interested are you in unconventional ideas and ways of doing things?", [
                "Not interested", "Slightly interested", "Moderately interested", "Very interested", "Extremely interested"]),
            ("How much do you enjoy appreciating or creating art, music, or literature?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How confident are you in your creative abilities?", [
                "Not confident", "Slightly confident", "Moderately confident", "Very confident", "Extremely confident"])
        ],
        'Social': [
            ("How much do you enjoy working with people?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How interested are you in helping others solve their problems?", [
                "Not interested", "Slightly interested", "Moderately interested", "Very interested", "Extremely interested"]),
            ("How comfortable are you in group settings?", [
                "Very uncomfortable", "Somewhat uncomfortable", "Neutral", "Comfortable", "Very comfortable"]),
            ("How much do you enjoy teaching or explaining things to others?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How interested are you in understanding people's motivations and behaviors?", [
                "Not interested", "Slightly interested", "Moderately interested", "Very interested", "Extremely interested"]),
            ("How much do you value cooperation and teamwork?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How comfortable are you with public speaking or performing?", [
                "Very uncomfortable", "Somewhat uncomfortable", "Neutral", "Comfortable", "Very comfortable"]),
            ("How interested are you in social issues and community service?", [
                "Not interested", "Slightly interested", "Moderately interested", "Very interested", "Extremely interested"]),
            ("How much do you enjoy organizing group activities or events?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How confident are you in your ability to communicate effectively with others?", [
                "Not confident", "Slightly confident", "Moderately confident", "Very confident", "Extremely confident"])
        ],
        'Enterprising': [
            ("How much do you enjoy leading or managing others?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How interested are you in starting your own business?", [
                "Not interested", "Slightly interested", "Moderately interested", "Very interested", "Extremely interested"]),
            ("How comfortable are you with taking risks?", [
                "Very uncomfortable", "Somewhat uncomfortable", "Neutral", "Comfortable", "Very comfortable"]),
            ("How much do you enjoy persuading or influencing others?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How interested are you in sales or marketing activities?", [
                "Not interested", "Slightly interested", "Moderately interested", "Very interested", "Extremely interested"]),
            ("How much do you value competition and achievement?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How comfortable are you with making important decisions?", [
                "Very uncomfortable", "Somewhat uncomfortable", "Neutral", "Comfortable", "Very comfortable"]),
            ("How interested are you in politics or economic systems?", [
                "Not interested", "Slightly interested", "Moderately interested", "Very interested", "Extremely interested"]),
            ("How much do you enjoy negotiating or debating?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How confident are you in your ability to motivate and lead others?", [
                "Not confident", "Slightly confident", "Moderately confident", "Very confident", "Extremely confident"])
        ],
        'Conventional': [
            ("How much do you enjoy working with numbers and data?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How interested are you in maintaining accurate records?", [
                "Not interested", "Slightly interested", "Moderately interested", "Very interested", "Extremely interested"]),
            ("How comfortable are you with following set procedures and routines?", [
                "Very uncomfortable", "Somewhat uncomfortable", "Neutral", "Comfortable", "Very comfortable"]),
            ("How much do you enjoy organizing and categorizing information?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How interested are you in working in an office environment?", [
                "Not interested", "Slightly interested", "Moderately interested", "Very interested", "Extremely interested"]),
            ("How much do you value attention to detail and accuracy?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How comfortable are you with using computer software for data management?", [
                "Very uncomfortable", "Somewhat uncomfortable", "Neutral", "Comfortable", "Very comfortable"]),
            ("How interested are you in financial or business operations?", [
                "Not interested", "Slightly interested", "Moderately interested", "Very interested", "Extremely interested"]),
            ("How much do you enjoy creating or following schedules and plans?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How confident are you in your ability to manage time and resources efficiently?", [
                "Not confident", "Slightly confident", "Moderately confident", "Very confident", "Extremely confident"])
        ]
    },
    'OCEAN': {
        'Openness': [
            ("How curious are you about various topics and ideas?", [
                "Not at all curious", "Slightly curious", "Moderately curious", "Very curious", "Extremely curious"]),
            ("How much do you enjoy trying new experiences?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How interested are you in abstract or philosophical discussions?", [
                "Not interested", "Slightly interested", "Moderately interested", "Very interested", "Extremely interested"]),
            ("How comfortable are you with change and variety in your life?", [
                "Very uncomfortable", "Somewhat uncomfortable", "Neutral", "Comfortable", "Very comfortable"]),
            ("How much do you value creativity and imagination?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"])
        ],
        'Conscientiousness': [
            ("How organized are you in your daily life and work?", [
                "Not at all organized", "Slightly organized", "Moderately organized", "Very organized", "Extremely organized"]),
            ("How much do you value punctuality and meeting deadlines?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How thorough are you when completing tasks or projects?", [
                "Not thorough at all", "Slightly thorough", "Moderately thorough", "Very thorough", "Extremely thorough"]),
            ("How much do you plan ahead before taking action?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How disciplined are you in pursuing your goals?", [
                "Not disciplined at all", "Slightly disciplined", "Moderately disciplined", "Very disciplined", "Extremely disciplined"])
        ],
        'Extraversion': [
            ("How much do you enjoy being around other people?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How comfortable are you in social situations?", [
                "Very uncomfortable", "Somewhat uncomfortable", "Neutral", "Comfortable", "Very comfortable"]),
            ("How often do you take the initiative in social interactions?", [
                "Never", "Rarely", "Sometimes", "Often", "Always"]),
            ("How energized do you feel after spending time with others?", [
                "Not at all energized", "Slightly energized", "Moderately energized", "Very energized", "Extremely energized"]),
            ("How much do you enjoy being the center of attention?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"])
        ],
        'Agreeableness': [
            ("How easily do you trust and get along with others?", [
                "Very difficult", "Somewhat difficult", "Neutral", "Somewhat easy", "Very easy"]),
            ("How much do you value harmony in your relationships?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How willing are you to compromise or cooperate with others?", [
                "Not willing at all", "Slightly willing", "Moderately willing", "Very willing", "Extremely willing"]),
            ("How much do you care about others' feelings and well-being?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How forgiving are you when someone wrongs you?", [
                "Not forgiving at all", "Slightly forgiving", "Moderately forgiving", "Very forgiving", "Extremely forgiving"])
        ],
        'Neuroticism': [
            ("How often do you experience stress or anxiety?", [
                "Never", "Rarely", "Sometimes", "Often", "Always"]),
            ("How easily do your moods change?", [
                "Not easily at all", "Somewhat easily", "Moderately easily", "Very easily", "Extremely easily"]),
            ("How much do you worry about things that might go wrong?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How sensitive are you to criticism or negative feedback?", [
                "Not sensitive at all", "Slightly sensitive", "Moderately sensitive", "Very sensitive", "Extremely sensitive"]),
            ("How often do you feel overwhelmed by your emotions?", [
                "Never", "Rarely", "Sometimes", "Often", "Always"])
        ]
    },
    'Hofstede': {
        'PDI': [
            ("How comfortable are you with hierarchical structures in organizations?", [
                "Very uncomfortable", "Somewhat uncomfortable", "Neutral", "Comfortable", "Very comfortable"]),
            ("How much do you believe in respecting authority figures?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How important is it for you to have clear directions from superiors?", [
                "Not important", "Slightly important", "Moderately important", "Very important", "Extremely important"]),
            ("How much do you value equality in power distribution?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How comfortable are you with challenging those in authority?", [
                "Very uncomfortable", "Somewhat uncomfortable", "Neutral", "Comfortable", "Very comfortable"])
        ],
        'IDV': [
            ("How much do you value individual achievements over group success?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How comfortable are you with standing out from the crowd?", [
                "Very uncomfortable", "Somewhat uncomfortable", "Neutral", "Comfortable", "Very comfortable"]),
            ("How important is personal time and space to you?", [
                "Not important", "Slightly important", "Moderately important", "Very important", "Extremely important"]),
            ("How much do you rely on yourself versus others for support?", [
                "Always rely on others", "Often rely on others", "Balance between self and others", "Often rely on self", "Always rely on self"]),
            ("How much do you prioritize your personal goals over group harmony?", [
                "Never", "Rarely", "Sometimes", "Often", "Always"])
        ],
        'MAS': [
            ("How much do you value competition and achievement in your work?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How important is it for you to be assertive and ambitious?", [
                "Not important", "Slightly important", "Moderately important", "Very important", "Extremely important"]),
            ("How much do you prioritize career success over work-life balance?", [
                "Always prioritize work-life balance", "Often prioritize work-life balance", "Equal priority", "Often prioritize career success", "Always prioritize career success"]),
            ("How comfortable are you with conflict and confrontation?", [
                "Very uncomfortable", "Somewhat uncomfortable", "Neutral", "Comfortable", "Very comfortable"]),
            ("How much do you believe in traditional gender roles?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"])
        ],
        'UAI': [
            ("How much do you prefer structure and clear rules in your life?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How uncomfortable do you feel in ambiguous or uncertain situations?", [
                "Not uncomfortable at all", "Slightly uncomfortable", "Moderately uncomfortable", "Very uncomfortable", "Extremely uncomfortable"]),
            ("How important is job security to you?", [
                "Not important", "Slightly important", "Moderately important", "Very important", "Extremely important"]),
            ("How much do you rely on experts and their knowledge?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How resistant are you to change and new ideas?", [
                "Not resistant at all", "Slightly resistant", "Moderately resistant", "Very resistant", "Extremely resistant"])
        ],
        'LTO': [
            ("How much do you value long-term planning over short-term gains?", [
                "Always prefer short-term", "Often prefer short-term", "Equal preference", "Often prefer long-term", "Always prefer long-term"]),
            ("How important is it for you to save and invest for the future?", [
                "Not important", "Slightly important", "Moderately important", "Very important", "Extremely important"]),
            ("How much do you believe in adapting traditions to new circumstances?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How patient are you in waiting for results or rewards?", [
                "Not patient at all", "Slightly patient", "Moderately patient", "Very patient", "Extremely patient"]),
            ("How much do you value perseverance in achieving goals?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"])
        ],
        'IVR': [
            ("How much do you prioritize enjoying life and having fun?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How freely do you express your desires and emotions?", [
                "Not freely at all", "Somewhat freely", "Moderately freely", "Very freely", "Extremely freely"]),
            ("How important is leisure time to you?", [
                "Not important", "Slightly important", "Moderately important", "Very important", "Extremely important"]),
            ("How much do you believe in following your impulses?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Extremely"]),
            ("How optimistic are you about life in general?", [
                "Not optimistic at all", "Slightly optimistic", "Moderately optimistic", "Very optimistic", "Extremely optimistic"])
        ]
    },
    'mbti_questions': {  #This section is not used in the program
        'E': [
            ("How energized do you feel by social interactions?", [
                "Not at all", "Slightly", "Moderately", "Very", "Extremely"]),
            ("How comfortable are you in large group settings?", [
                "Not comfortable at all", "Slightly comfortable", "Moderately comfortable", "Very comfortable", "Extremely comfortable"]),
            ("How much do you enjoy being the center of attention?", [
                "Not at all", "Slightly", "Moderately", "Very much", "Extremely"]),
            ("How often do you initiate conversations with strangers?", [
                "Never", "Rarely", "Sometimes", "Often", "Very often"]),
            ("How energized do you feel after attending a social event?", [
                "Not at all", "Slightly", "Moderately", "Very", "Extremely"])
        ],
        'S': [
            ("How much do you rely on concrete facts and details?", [
                "Not at all", "Slightly", "Moderately", "Very much", "Extremely"]),
            ("How focused are you on the present moment?", [
                "Not focused at all", "Slightly focused", "Moderately focused", "Very focused", "Extremely focused"]),
            ("How much do you trust your direct experiences?", [
                "Not at all", "Somewhat", "Moderately", "Very much", "Completely"]),
            ("How practical is your approach to problem-solving?", [
                "Not practical at all", "Somewhat practical", "Moderately practical", "Very practical", "Extremely practical"]),
            ("How much do you prefer step-by-step instructions?", [
                "Not at all", "Slightly", "Moderately", "Very much", "Extremely"])
        ],
        'T': [
            ("How much do you rely on logic when making decisions?", [
                "Not at all", "Slightly", "Moderately", "Very much", "Extremely"]),
            ("How important is objectivity to you?", [
                "Not important", "Slightly important", "Moderately important", "Very important", "Extremely important"]),
            ("How comfortable are you with critiquing others?", [
                "Not comfortable at all", "Slightly comfortable", "Moderately comfortable", "Very comfortable", "Extremely comfortable"]),
            ("How much do you value efficiency over harmony?", [
                "Not at all", "Slightly", "Moderately", "Very much", "Extremely"]),
            ("How analytical is your approach to problems?", [
                "Not analytical at all", "Slightly analytical", "Moderately analytical", "Very analytical", "Extremely analytical"])
        ],
        'J': [
            ("How much do you prefer having a structured schedule?", [
                "Not at all", "Slightly", "Moderately", "Very much", "Extremely"]),
            ("How important is it for you to complete tasks well before deadlines?", [
                "Not important", "Slightly important", "Moderately important", "Very important", "Extremely important"]),
            ("How much do you like planning ahead?", [
                "Not at all", "Slightly", "Moderately", "Very much", "Extremely"]),
            ("How uncomfortable do you feel with open-ended situations?", [
                "Not uncomfortable at all", "Slightly uncomfortable", "Moderately uncomfortable", "Very uncomfortable", "Extremely uncomfortable"]),
            ("How much do you prefer having clear rules and guidelines?", [
                "Not at all", "Slightly", "Moderately", "Very much", "Extremely"])
        ]
    }
}


aptitude_questions = {
    'V': [
        ("Choose the word most similar in meaning to 'Benevolent':", ["Malicious", "Charitable", "Arrogant", "Indifferent"], "Charitable"),
        ("Complete the analogy: Book is to Reading as Fork is to:", ["Eating", "Cooking", "Cutting", "Stirring"], "Eating"),
        ("Which word is the opposite of 'Frugal'?", ["Wasteful", "Careful", "Economical", "Prudent"], "Wasteful"),
        ("Choose the word that best completes the sentence: The detective's _____ search of the crime scene yielded important evidence.", ["Cursory", "Thorough", "Brief", "Hasty"], "Thorough"),
        ("What is the meaning of 'Ubiquitous'?", ["Rare", "Everywhere", "Unique", "Scarce"], "Everywhere"),
        ("Which word is a synonym for 'Eloquent'?", ["Articulate", "Shy", "Silent", "Clumsy"], "Articulate"),
        ("Complete the analogy: Light is to Dark as Loud is to:", ["Quiet", "Noisy", "Bright", "Dim"], "Quiet"),
        ("Choose the word that doesn't belong:", ["Ecstatic", "Elated", "Jubilant", "Melancholy"], "Melancholy")
    ],
    'Nu': [
        ("What is 15% of 80?", ["10", "12", "15", "18"], "12"),
        ("If x + 2 = 7, what is the value of x?", ["3", "4", "5", "6"], "5"),
        ("What is the next number in the sequence: 2, 4, 8, 16, ...?", ["24", "32", "64", "128"], "32"),
        ("If a shirt costs $25 and is on sale for 20% off, what is the sale price?", ["$15", "$18", "$20", "$22"], "20"),
        ("What is the square root of 144?", ["10", "11", "12", "13"], "12"),
        ("If 3x - 5 = 16, what is x?", ["5", "6", "7", "8"], "7"),
        ("What is 3/4 expressed as a decimal?", ["0.25", "0.50", "0.75", "0.80"], "0.75"),
        ("If a car travels 120 miles in 2 hours, what is its average speed in miles per hour?", ["30", "40", "60", "80"], "60")
    ],
    'Sp': [
        ("Which shape would complete the pattern?", ["Square", "Triangle", "Circle", "Pentagon"], "Triangle"),
        ("If you unfold a cube, how many squares will you see?", ["4", "5", "6", "7"], "6"),
        ("Which 3D shape has 6 faces, 8 vertices, and 12 edges?", ["Cube", "Sphere", "Pyramid", "Cylinder"], "Cube"),
        ("Which image is the correct rotation of the given object?", ["Image A", "Image B", "Image C", "Image D"], "Image C"),
        ("How many cubes are needed to build this structure?", ["8", "10", "12", "14"], "12"),
        ("Which of these is not a possible net of a cube?", ["Net A", "Net B", "Net C", "Net D"], "Net B"),
        ("If you look at this object from above, which shape would you see?", ["Circle", "Square", "Triangle", "Rectangle"], "Square"),
        ("Which piece completes the puzzle?", ["Piece A", "Piece B", "Piece C", "Piece D"], "Piece C")
    ],
    'LR': [
        ("If all A are B, and some B are C, then:", ["All A are C", "Some A are C", "No A are C", "None of the above"], "Some A are C"),
        ("Which number should come next in this series? 1, 3, 6, 10, 15, ...", ["21", "22", "23", "24"], "21"),
        ("If 'some cats are animals' and 'all animals are living things', which statement must be true?", ["All cats are living things", "Some cats are living things", "No cats are living things", "All living things are cats"], "Some cats are living things"),
        ("In a race, if you pass the person in 2nd place, what place are you in now?", ["1st", "2nd", "3rd", "4th"], "2nd"),
        ("If it's true that 'if it's raining, then the ground is wet', and the ground is not wet, what can you conclude?", ["It's raining", "It's not raining", "The ground is dry", "Not enough information"], "It's not raining"),
        ("Which word does not belong in this group?", ["Apple", "Banana", "Carrot", "Orange"], "Carrot"),
        ("If you rearrange the letters 'CIFAIPC', you would have the name of a(n):", ["Country", "Animal", "Ocean", "City"], "Ocean"),
        ("What number is missing: 4, 9, 16, 25, _, 49", ["30", "36", "40", "45"], "36")
    ],
    'Me': [
        ("Which tool is best for tightening a bolt?", ["Hammer", "Screwdriver", "Wrench", "Pliers"], "Wrench"),
        ("In which direction would a gear turn if the gear next to it is turning clockwise?", ["Clockwise", "Counter-clockwise", "It wouldn't turn", "Depends on the size"], "Counter-clockwise"),
        ("What simple machine is a knife an example of?", ["Lever", "Wedge", "Pulley", "Wheel and axle"], "Wedge"),
        ("Which of these is not a type of simple machine?", ["Inclined plane", "Screw", "Magnet", "Lever"], "Magnet"),
        ("What happens to the speed of a pulley system when you add more pulleys?", ["Increases", "Decreases", "Stays the same", "Becomes unpredictable"], "Decreases"),
        ("Which of these would create the most friction?", ["Smooth metal on smooth metal", "Rubber on concrete", "Wood on wax", "Glass on glass"], "Rubber on concrete"),
        ("What type of energy does a stretched rubber band have?", ["Kinetic", "Potential", "Thermal", "Nuclear"], "Potential"),
        ("In a class 1 lever, where is the fulcrum located?", ["At one end", "In the middle", "At both ends", "There is no fulcrum"], "In the middle")
    ],
    'Pe': [
        ("Which image is different from the others?", ["Image A", "Image B", "Image C", "Image D"], "Image C"),
        ("How many triangles can you find in this image?", ["5", "6", "7", "8"], "7"),
        ("Which pattern comes next in the sequence?", ["Pattern A", "Pattern B", "Pattern C", "Pattern D"], "Pattern B"),
        ("Find the odd one out:", ["Image 1", "Image 2", "Image 3", "Image 4"], "Image 3"),
        ("Which piece completes the pattern?", ["Piece A", "Piece B", "Piece C", "Piece D"], "Piece C"),
        ("How many faces does this 3D object have?", ["4", "5", "6", "7"], "6"),
        ("Which image is the mirror reflection of the given image?", ["Image W", "Image X", "Image Y", "Image Z"], "Image Y"),
        ("Count the number of squares in this figure:", ["14", "16", "18", "20"], "18")
    ],
    'Ab': [
        ("Complete the sequence: 2, 6, 12, 20, ?", ["30", "32", "36", "42"], "30"),
        ("If RED is coded as 27 and BLUE is coded as 37, what is the code for GREEN?", ["47", "57", "67", "77"], "57"),
        ("Which figure completes the pattern?", ["Figure A", "Figure B", "Figure C", "Figure D"], "Figure C"),
        ("What comes next in the pattern: AZ, BY, CX, ?", ["DW", "DV", "EW", "EV"], "DW"),
        ("If YZABC stands for 43210, what does ABCYZ stand for?", ["21043", "01234", "43201", "23410"], "01234"),
        ("Which number does not belong in the series? 2, 5, 10, 17, 26, 37, 50", ["17", "26", "37", "50"], "37"),
        ("If you rearrange the letters 'RAPETEKA', you get the name of a:", ["Country", "Animal", "Fruit", "Profession"], "Fruit"),
        ("What is the missing number: 8 : 4 :: 18 : 6 :: 32 : ?", ["8", "10", "12", "16"], "8")
    ]
}

#aptitude
career_cluster_weights = {
    "Agricultural & Food Sciences": {
        'V': 6, 'Nu': 7, 'Sp': 7, 'LR': 8, 'Me': 8, 'Pe': 7, 'Ab': 7
    },
    "Medical Sciences": {
        'V': 8, 'Nu': 8, 'Sp': 7, 'LR': 9, 'Me': 7, 'Pe': 9, 'Ab': 8
    },
    "Allied & Paramedical Sciences": {
        'V': 7, 'Nu': 7, 'Sp': 6, 'LR': 8, 'Me': 6, 'Pe': 9, 'Ab': 7
    },
    "Humanities, Liberal Arts & Social Sciences": {
        'V': 10, 'Nu': 6, 'Sp': 5, 'LR': 8, 'Me': 3, 'Pe': 7, 'Ab': 8
    },
    "Journalism & Mass Communication": {
        'V': 10, 'Nu': 5, 'Sp': 6, 'LR': 8, 'Me': 3, 'Pe': 8, 'Ab': 7
    },
    "Design, Animation, Graphics & Applied Arts": {
        'V': 7, 'Nu': 6, 'Sp': 10, 'LR': 8, 'Me': 7, 'Pe': 9, 'Ab': 9
    },
    "Performing Arts": {
        'V': 8, 'Nu': 4, 'Sp': 7, 'LR': 6, 'Me': 5, 'Pe': 9, 'Ab': 8
    },
    "Hospitality, Tourism Services": {
        'V': 9, 'Nu': 6, 'Sp': 5, 'LR': 7, 'Me': 4, 'Pe': 8, 'Ab': 6
    },
    "Business Management & Marketing": {
        'V': 9, 'Nu': 8, 'Sp': 5, 'LR': 9, 'Me': 4, 'Pe': 7, 'Ab': 8
    },
    "Commerce & BFSI": {
        'V': 7, 'Nu': 10, 'Sp': 5, 'LR': 9, 'Me': 3, 'Pe': 7, 'Ab': 8
    },
    "Entrepreneurship": {
        'V': 8, 'Nu': 8, 'Sp': 6, 'LR': 9, 'Me': 5, 'Pe': 7, 'Ab': 9
    },
    "Economics": {
        'V': 8, 'Nu': 10, 'Sp': 5, 'LR': 9, 'Me': 3, 'Pe': 6, 'Ab': 9
    },
    "Architecture & Planning": {
        'V': 7, 'Nu': 8, 'Sp': 10, 'LR': 8, 'Me': 7, 'Pe': 9, 'Ab': 8
    },
    "IT & CS & AI & Data Science": {
        'V': 7, 'Nu': 9, 'Sp': 7, 'LR': 10, 'Me': 6, 'Pe': 8, 'Ab': 9
    },
    "Engineering": {
        'V': 7, 'Nu': 9, 'Sp': 8, 'LR': 9, 'Me': 9, 'Pe': 7, 'Ab': 8
    },
    "Physical Science, Life Science & Environment": {
        'V': 7, 'Nu': 9, 'Sp': 7, 'LR': 9, 'Me': 7, 'Pe': 7, 'Ab': 9
    },
    "Mathematics & Statistics & Actuary": {
        'V': 6, 'Nu': 10, 'Sp': 6, 'LR': 10, 'Me': 4, 'Pe': 7, 'Ab': 9
    },
    "Govt & Defense Services": {
        'V': 8, 'Nu': 7, 'Sp': 7, 'LR': 8, 'Me': 7, 'Pe': 8, 'Ab': 7
    },
    "Education & Teaching": {
        'V': 9, 'Nu': 7, 'Sp': 6, 'LR': 8, 'Me': 5, 'Pe': 8, 'Ab': 8
    },
    "Legal Services": {
        'V': 10, 'Nu': 6, 'Sp': 5, 'LR': 10, 'Me': 3, 'Pe': 7, 'Ab': 9
    }
}


career_clusters = {
    "Agricultural & Food Sciences": {
        'RIASEC': {"Realistic": 8, "Investigative": 7, "Artistic": 3, "Social": 5, "Enterprising": 4, "Conventional": 6},
        'OCEAN': {"Openness": 6, "Conscientiousness": 8, "Extraversion": 6, "Agreeableness": 6, "Neuroticism": 4},
        'Hofstede': {"PDI": 6, "IDV": 5, "MAS": 6, "UAI": 7, "LTO": 8, "IVR": 5},
        'Aptitude': career_cluster_weights["Agricultural & Food Sciences"]  # Use weights directly
    },
    "Medical Sciences": {
        'RIASEC': {"Realistic": 6, "Investigative": 9, "Artistic": 3, "Social": 8, "Enterprising": 5, "Conventional": 7},
        'OCEAN': {"Openness": 7, "Conscientiousness": 9, "Extraversion": 7, "Agreeableness": 8, "Neuroticism": 3},
        'Hofstede': {"PDI": 5, "IDV": 6, "MAS": 7, "UAI": 9, "LTO": 8, "IVR": 4},
        'Aptitude': career_cluster_weights["Medical Sciences"]
    },
    "Allied & Paramedical Sciences": {
        'RIASEC': {"Realistic": 7, "Investigative": 8, "Artistic": 3, "Social": 9, "Enterprising": 4, "Conventional": 6},
        'OCEAN': {"Openness": 6, "Conscientiousness": 8, "Extraversion": 7, "Agreeableness": 9, "Neuroticism": 3},
        'Hofstede': {"PDI": 5, "IDV": 6, "MAS": 6, "UAI": 8, "LTO": 7, "IVR": 5},
        'Aptitude': career_cluster_weights["Allied & Paramedical Sciences"]
    },
    "Life Science & Environment": {
        'RIASEC': {"Realistic": 6, "Investigative": 9, "Artistic": 4, "Social": 5, "Enterprising": 3, "Conventional": 7},
        'OCEAN': {"Openness": 8, "Conscientiousness": 8, "Extraversion": 5, "Agreeableness": 6, "Neuroticism": 4},
        'Hofstede': {"PDI": 4, "IDV": 7, "MAS": 5, "UAI": 7, "LTO": 9, "IVR": 6},
        'Aptitude': career_cluster_weights["Physical Science, Life Science & Environment"]
    },
    "Humanities, Liberal Arts & Social Sciences": {
        'RIASEC': {"Realistic": 2, "Investigative": 7, "Artistic": 6, "Social": 8, "Enterprising": 5, "Conventional": 4},
        'OCEAN': {"Openness": 9, "Conscientiousness": 7, "Extraversion": 6, "Agreeableness": 8, "Neuroticism": 5},
        'Hofstede': {"PDI": 3, "IDV": 8, "MAS": 4, "UAI": 5, "LTO": 7, "IVR": 7},
        'Aptitude': career_cluster_weights["Humanities, Liberal Arts & Social Sciences"]
    },
    "Animation, Graphics & Applied Arts": {
        'RIASEC': {"Realistic": 5, "Investigative": 4, "Artistic": 10, "Social": 3, "Enterprising": 5, "Conventional": 6},
        'OCEAN': {"Openness": 9, "Conscientiousness": 7, "Extraversion": 5, "Agreeableness": 6, "Neuroticism": 5},
        'Hofstede': {"PDI": 3, "IDV": 8, "MAS": 5, "UAI": 4, "LTO": 6, "IVR": 8},
        'Aptitude': career_cluster_weights["Design, Animation, Graphics & Applied Arts"]
    },
    "Journalism & Mass Communication": {
        'RIASEC': {"Realistic": 3, "Investigative": 6, "Artistic": 7, "Social": 8, "Enterprising": 7, "Conventional": 5},
        'OCEAN': {"Openness": 8, "Conscientiousness": 7, "Extraversion": 8, "Agreeableness": 7, "Neuroticism": 5},
        'Hofstede': {"PDI": 4, "IDV": 8, "MAS": 7, "UAI": 5, "LTO": 6, "IVR": 8},
        'Aptitude': career_cluster_weights["Journalism & Mass Communication"]
    },
    "Design": {
        'RIASEC': {"Realistic": 5, "Investigative": 5, "Artistic": 10, "Social": 4, "Enterprising": 6, "Conventional": 5},
        'OCEAN': {"Openness": 9, "Conscientiousness": 8, "Extraversion": 6, "Agreeableness": 6, "Neuroticism": 4},
        'Hofstede': {"PDI": 3, "IDV": 8, "MAS": 6, "UAI": 4, "LTO": 7, "IVR": 8},
        'Aptitude': career_cluster_weights["Design, Animation, Graphics & Applied Arts"]
    },
    "Performing Arts": {
        'RIASEC': {"Realistic": 4, "Investigative": 3, "Artistic": 10, "Social": 6, "Enterprising": 5, "Conventional": 2},
        'OCEAN': {"Openness": 9, "Conscientiousness": 8, "Extraversion": 8, "Agreeableness": 7, "Neuroticism": 6},
        'Hofstede': {"PDI": 2, "IDV": 9, "MAS": 6, "UAI": 3, "LTO": 6, "IVR": 9},
        'Aptitude': career_cluster_weights["Performing Arts"]
    },
    "Hospitality, Tourism Services": {
        'RIASEC': {"Realistic": 5, "Investigative": 4, "Artistic": 5, "Social": 9, "Enterprising": 8, "Conventional": 6},
        'OCEAN': {"Openness": 7, "Conscientiousness": 8, "Extraversion": 9, "Agreeableness": 9, "Neuroticism": 3},
        'Hofstede': {"PDI": 5, "IDV": 7, "MAS": 6, "UAI": 6, "LTO": 6, "IVR": 8},
        'Aptitude': career_cluster_weights["Hospitality, Tourism Services"]
    },
    "Business Management & Marketing": {
        'RIASEC': {"Realistic": 3, "Investigative": 6, "Artistic": 5, "Social": 7, "Enterprising": 9, "Conventional": 7},
        'OCEAN': {"Openness": 7, "Conscientiousness": 8, "Extraversion": 8, "Agreeableness": 7, "Neuroticism": 4},
        'Hofstede': {"PDI": 6, "IDV": 8, "MAS": 8, "UAI": 6, "LTO": 7, "IVR": 7},
        'Aptitude': career_cluster_weights["Business Management & Marketing"]
    },
    "Commerce": {
        'RIASEC': {"Realistic": 3, "Investigative": 6, "Artistic": 3, "Social": 5, "Enterprising": 8, "Conventional": 9},
        'OCEAN': {"Openness": 6, "Conscientiousness": 9, "Extraversion": 7, "Agreeableness": 6, "Neuroticism": 3},
        'Hofstede': {"PDI": 6, "IDV": 7, "MAS": 8, "UAI": 7, "LTO": 7, "IVR": 6},
        'Aptitude': career_cluster_weights["Commerce & BFSI"]
    },
    "BFSI (Banking, Financial Services, Insurance)": {
        'RIASEC': {"Realistic": 2, "Investigative": 7, "Artistic": 2, "Social": 5, "Enterprising": 8, "Conventional": 10},
        'OCEAN': {"Openness": 6, "Conscientiousness": 9, "Extraversion": 6, "Agreeableness": 6, "Neuroticism": 3},
        'Hofstede': {"PDI": 7, "IDV": 7, "MAS": 8, "UAI": 8, "LTO": 8, "IVR": 4},
        'Aptitude': career_cluster_weights["Commerce & BFSI"]
    },
    "Entrepreneurship": {
        'RIASEC': {"Realistic": 5, "Investigative": 6, "Artistic": 6, "Social": 7, "Enterprising": 10, "Conventional": 5},
        'OCEAN': {"Openness": 9, "Conscientiousness": 9, "Extraversion": 8, "Agreeableness": 7, "Neuroticism": 5},
        'Hofstede': {"PDI": 3, "IDV": 9, "MAS": 8, "UAI": 4, "LTO": 7, "IVR": 8},
        'Aptitude': career_cluster_weights["Entrepreneurship"]
    },
    "Economics": {
        'RIASEC': {"Realistic": 2, "Investigative": 9, "Artistic": 3, "Social": 5, "Enterprising": 7, "Conventional": 8},
        'OCEAN': {"Openness": 7, "Conscientiousness": 8, "Extraversion": 6, "Agreeableness": 6, "Neuroticism": 4},
        'Hofstede': {"PDI": 5, "IDV": 8, "MAS": 7, "UAI": 7, "LTO": 9, "IVR": 5},
        'Aptitude': career_cluster_weights["Economics"]
    },
    "Architecture & Planning": {
        'RIASEC': {"Realistic": 7, "Investigative": 7, "Artistic": 9, "Social": 5, "Enterprising": 6, "Conventional": 7},
        'OCEAN': {"Openness": 8, "Conscientiousness": 9, "Extraversion": 6, "Agreeableness": 7, "Neuroticism": 4},
        'Hofstede': {"PDI": 5, "IDV": 7, "MAS": 7, "UAI": 6, "LTO": 8, "IVR": 6},
        'Aptitude': career_cluster_weights["Architecture & Planning"]
    },
    "IT & Computer Science": {
        'RIASEC': {"Realistic": 6, "Investigative": 9, "Artistic": 5, "Social": 3, "Enterprising": 5, "Conventional": 8},
        'OCEAN': {"Openness": 7, "Conscientiousness": 8, "Extraversion": 5, "Agreeableness": 6, "Neuroticism": 4},
        'Hofstede': {"PDI": 4, "IDV": 8, "MAS": 7, "UAI": 5, "LTO": 8, "IVR": 6},
        'Aptitude': career_cluster_weights["IT & CS & AI & Data Science"]
    },
    "AI & Data Science & Blockchain": {
        'RIASEC': {"Realistic": 4, "Investigative": 10, "Artistic": 4, "Social": 2, "Enterprising": 5, "Conventional": 8},
        'OCEAN': {"Openness": 8, "Conscientiousness": 9, "Extraversion": 5, "Agreeableness": 5, "Neuroticism": 3},
        'Hofstede': {"PDI": 3, "IDV": 9, "MAS": 7, "UAI": 4, "LTO": 9, "IVR": 6},
        'Aptitude': career_cluster_weights["IT & CS & AI & Data Science"]
    },
    "Engineering": {
        'RIASEC': {"Realistic": 8, "Investigative": 9, "Artistic": 5, "Social": 4, "Enterprising": 5, "Conventional": 7},
        'OCEAN': {"Openness": 7, "Conscientiousness": 9, "Extraversion": 6, "Agreeableness": 6, "Neuroticism": 3},
        'Hofstede': {"PDI": 5, "IDV": 7, "MAS": 8, "UAI": 7, "LTO": 8, "IVR": 5},
        'Aptitude': career_cluster_weights["Engineering"]
    },
    "Physical Science": {
        'RIASEC': {"Realistic": 6, "Investigative": 10, "Artistic": 3, "Social": 2, "Enterprising": 3, "Conventional": 7},
        'OCEAN': {"Openness": 8, "Conscientiousness": 9, "Extraversion": 5, "Agreeableness": 5, "Neuroticism": 3},
        'Hofstede': {"PDI": 3, "IDV": 8, "MAS": 6, "UAI": 6, "LTO": 9, "IVR": 5},
        'Aptitude': career_cluster_weights["Physical Science, Life Science & Environment"]
    },
    "Mathematics & Statistics & Actuary": {
        'RIASEC': {"Realistic": 3, "Investigative": 10, "Artistic": 2, "Social": 2, "Enterprising": 4, "Conventional": 9},
        'OCEAN': {"Openness": 7, "Conscientiousness": 9, "Extraversion": 4, "Agreeableness": 5, "Neuroticism": 3},
        'Hofstede': {"PDI": 4, "IDV": 7, "MAS": 6, "UAI": 8, "LTO": 9, "IVR": 4},
        'Aptitude': career_cluster_weights["Mathematics & Statistics & Actuary"]
    },
    "Govt & Defense Services": {
        'RIASEC': {"Realistic": 7, "Investigative": 6, "Artistic": 2, "Social": 7, "Enterprising": 7, "Conventional": 8},
        'OCEAN': {"Openness": 6, "Conscientiousness": 9, "Extraversion": 7, "Agreeableness": 7, "Neuroticism": 3},
        'Hofstede': {"PDI": 7, "IDV": 5, "MAS": 7, "UAI": 8, "LTO": 7, "IVR": 4},
        'Aptitude': career_cluster_weights["Govt & Defense Services"]
    },
    "Education & Teaching": {
        'RIASEC': {"Realistic": 4, "Investigative": 7, "Artistic": 5, "Social": 10, "Enterprising": 6, "Conventional": 6},
        'OCEAN': {"Openness": 8, "Conscientiousness": 8, "Extraversion": 7, "Agreeableness": 9, "Neuroticism": 4},
        'Hofstede': {"PDI": 4, "IDV": 6, "MAS": 5, "UAI": 6, "LTO": 8, "IVR": 7},
        'Aptitude': career_cluster_weights["Education & Teaching"]
    },
    "Legal Services": {
        'RIASEC': {"Realistic": 2, "Investigative": 8, "Artistic": 3, "Social": 7, "Enterprising": 7, "Conventional": 9},
        'OCEAN': {"Openness": 7, "Conscientiousness": 9, "Extraversion": 7, "Agreeableness": 7, "Neuroticism": 4},
        'Hofstede': {"PDI": 6, "IDV": 7, "MAS": 8, "UAI": 8, "LTO": 7, "IVR": 5},
        'Aptitude': career_cluster_weights["Legal Services"]
    }
}

# In questionnaire.py

career_descriptions = {
    "Agricultural & Food Sciences": "This field focuses on the science and technology of producing and refining plants and animals for human use. It encompasses areas such as crop cultivation, livestock management, food processing, and agricultural economics.",

    "Medical Sciences": "Medical Sciences involve the study of preventing, diagnosing, and treating human diseases. This field includes various specialties such as general medicine, surgery, pediatrics, and emerging areas like genetic medicine.",

    "Allied & Paramedical Sciences": "These sciences support the core medical field and include disciplines such as nursing, physiotherapy, occupational therapy, and medical laboratory technology. Professionals in this field play crucial roles in patient care and medical support.",

    "Life Science & Environment": "This field studies living organisms and their interactions with each other and their environment. It includes subjects like biology, ecology, and environmental science, addressing crucial issues such as biodiversity and climate change.",

    "Humanities, Liberal Arts & Social Sciences": "These disciplines study human society and culture. They include subjects like history, philosophy, sociology, and psychology, fostering critical thinking, cultural understanding, and social analysis skills.",

    "Animation, Graphics & Applied Arts": "This creative field combines artistic skills with technology to create visual content for entertainment, advertising, and communication. It includes 2D and 3D animation, graphic design, and digital art.",

    "Journalism & Mass Communication": "This field focuses on gathering, analyzing, and disseminating information through various media channels. It covers print, broadcast, and digital journalism, as well as public relations and advertising.",

    "Design": "Design encompasses various disciplines that focus on creating functional and aesthetic solutions. It includes industrial design, fashion design, interior design, and user experience design, blending creativity with practical problem-solving.",

    "Performing Arts": "This field involves live performance before an audience, including theater, dance, music, and other forms of artistic expression. It combines creative talent with technical skills in areas like choreography, direction, and performance.",

    "Hospitality, Tourism Services": "This sector focuses on providing services to travelers and guests. It includes hotel management, event planning, tour operations, and culinary arts, emphasizing customer service and cultural sensitivity.",

    "Business Management & Marketing": "This field deals with the organization, planning, and management of businesses. It covers areas such as strategic planning, human resources, operations management, and marketing strategies to promote products and services.",

    "Commerce": "Commerce involves the study of business activities including trade, finance, and economics. It prepares students for careers in accounting, business administration, and financial analysis.",

    "BFSI (Banking, Financial Services, Insurance)": "This sector encompasses services related to money management. It includes retail and commercial banking, investment management, insurance, and emerging fintech services.",

    "Entrepreneurship": "Entrepreneurship focuses on the creation and management of new businesses. It involves identifying opportunities, developing business plans, securing funding, and managing startup operations.",

    "Economics": "Economics studies how societies allocate scarce resources. It includes microeconomics, macroeconomics, and econometrics, preparing students for careers in policy analysis, market research, and financial forecasting.",

    "Architecture & Planning": "This field combines art and science to design buildings and urban spaces. It includes architectural design, urban planning, landscape architecture, and sustainable development practices.",

    "IT & Computer Science": "This field deals with the theory and practice of computer-based systems. It covers software development, network administration, cybersecurity, and emerging technologies like cloud computing.",

    "AI & Data Science & Blockchain": "This cutting-edge field focuses on developing intelligent systems, analyzing large datasets, and creating secure, decentralized digital ledgers. It's at the forefront of technological innovation across various industries.",

    "Engineering": "Engineering applies scientific and mathematical principles to design, develop, and create products and systems. It includes various branches such as mechanical, electrical, civil, and chemical engineering.",

    "Physical Science": "Physical Science studies non-living systems and includes disciplines like physics and chemistry. It forms the basis for understanding the fundamental laws governing the universe and matter.",

    "Mathematics & Statistics & Actuary": "This field involves the study of numbers, quantities, and space. It includes pure mathematics, applied mathematics, statistics, and actuarial science, crucial for data analysis and risk assessment.",

    "Govt & Defense Services": "This sector involves working in public administration, policy-making, and national security. It includes civil services, military careers, and roles in government agencies and defense organizations.",

    "Education & Teaching": "This field focuses on imparting knowledge and skills to others. It includes teaching at various levels, educational administration, curriculum development, and emerging areas like e-learning and special education.",

    "Legal Services": "Legal Services involve the study and practice of law. It includes various specializations such as corporate law, criminal law, intellectual property law, and international law, preparing individuals for roles as lawyers, judges, or legal consultants."
}
        
