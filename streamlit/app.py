import streamlit as st
from streamlit_option_menu import option_menu
import json
import pandas as pd
import matplotlib
from test import *
from Custom_Diet import *
from PIL import Image
import sqlite3
import matplotlib.pyplot as plt
from db_operations import get_all_contact_messages, get_all_diets, get_all_medicines, get_all_workouts, \
    insert_contact_message


def read_image(file_path):
    """Reads an image file and returns its binary data as a BLOB."""
    with open(file_path, "rb") as file:
        return file.read()


# Function to initialize the database and create the required tables
def init_db():
    # Connect to SQLite database (this will create the db if it doesn't exist)
    conn = sqlite3.connect("fitness.db", timeout=10, check_same_thread=False)  # Prevent locking issues
    cursor = conn.cursor()

    # Drop old tables if needed
    cursor.execute("DROP TABLE IF EXISTS user_data")
    # Create user_data table
    cursor.execute('''
         CREATE TABLE IF NOT EXISTS user_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            age INTEGER,
            level TEXT,
            workout_plan TEXT
        )
    ''')

    # Create contact_messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute("DROP TABLE IF EXISTS diets")

    # Create diets table with the updated schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS diets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            name TEXT,
            dosage TEXT,
            frequency TEXT,
            side_effects TEXT
        )
    ''')

    # Create medicines table
    cursor.execute("DROP TABLE IF EXISTS medicines")
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS medicines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        disease_name TEXT,
        medicine_name TEXT,
        dosage_form TEXT,
        strength TEXT,
        instructions TEXT
    )
''')

    # Create workouts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            name TEXT,
            description TEXT,
            level TEXT,
            duration INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS progress_tracker (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            weight REAL,
            calories_burned REAL,
            diet TEXT,
            workout TEXT,
            progress TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
     CREATE TABLE IF NOT EXISTS Gym (
	    Day TEXT NOT NULL,
        Exercise TEXT NOT NULL,
        Sets TEXT,
        Reps TEXT
        )
    ''')
    cursor.execute('''
    INSERT INTO Gym VALUES  ('lower', '01', '3', '8-10'),
						('lower', '02', '3', '15-20'),
						('lower', '03', '3', '12-15'),
						('lower', '04', '3', '15-20'),
						('lower', '05', '3', '8-10'),
						('lower', '06', '3', '15-20'),
						('upper', '07', '3', '8-10'),
						('upper', '08', '3', '10-12'),
						('upper', '09', '3', '8-10'),
						('upper', '10', '3', '10'),
						('upper', '11', '3', '10-12'),
						('upper', '12', '3', '10')
    ''')
    cursor.execute(''' 
    CREATE TABLE if not exists Exercise (
	Id TEXT PRIMARY KEY NOT NULL,
    Name TEXT,
    Link TEXT,
    Overview TEXT,
    Introductions TEXT)

    ''')
    cursor.execute('''
    INSERT OR IGNORE INTO Exercise VALUES ('01', 'Squats', 'https://www.youtube.com/embed/R2dMsNhN3DE', 'The squat is the king of all exercises, working over 256 muscles in one movement! From bodybuilders to powerlifters to competitive athletes, the squat is a staple compound exercise and should be in every workout plan.;For powerlifters, it is known as one of the “big three” lifts which includes the squat, deadlift, and bench press. For athletes, having an explosive squat is a good indicator for on field/court performance. And for bodybuilders, the squat is a compound exercise that targets nearly every muscle of your lower body and core.;The squat directly targets the muscles of the quads, but also involves the hamstrings, glutes, back, and core as well as muscles of the shoulders and arms to a lesser degree.;Not everyone is built to perform the traditional barbell back squat and it can result in some pain for certain individuals. Over the years, several squatting variations have been developed to help everyone be able to train this critical movement pattern safely.;The emphasis of the squat can be switched from the quads to the hamstrings by your foot placement. Some wear shoes with an elevated heel (or elevate their heels on plates) to focus more on the quads. Others keep a flat foot to put more pressure on the hamstrings.;At the end of the day it is important that you pick a squat variation and foot placement that works best for you and that you can perform safely.'
																						, 'Set up for the exercise by setting the barbell to just below shoulder height and loading the weight you want to use.;Stand under the bar with your feet at about shoulder width apart.;Position the bar so that it is resting on the muscles on the top of your back, not on the back of your neck. The bar should feel comfortable. If it doesn''t, try adding some padding to the bar.;Now take your hands over the back and grip the bar with a wide grip for stability.;You should now bend at the knees and straighten your back in preparation to take the weight off the rack.;Keeping your back straight and eyes up, push up through the legs and take the weight off the rack.;Take a small step back and stabilize yourself.;Keeping your eyes facing forward slowly lower your body down. Don''t lean forward as you come down. Your buttocks should come out and drop straight down.;Squat down until your thighs are parallel with the floor, and then slowly raise your body back up by pushing through your heels.;Do not lock the knees out when you stand up, and then repeat the movement.'),
							('02', 'Leg Press', 'https://www.youtube.com/embed/sEM_zo9w2ss', 'The leg press is a variation of the squat and an exercise used to target the muscles of the leg.;One can utilize the leg press to target both the quads and the hamstring muscle, depending on which portion of the foot they push through.;The leg press is commonly thought of as a machine variation of the barbell back squat. The mechanics are fairly similar, however, the leg press does not completely mimic the movement pattern of the squat. Nor does it work all of the muscle groups that the squat does.;The leg press is best used as an accessory movement to the squat, or as a primary movement in gyms which lack the necessary equipment to train the squat movement pattern.'
																						   , 'Load the machine with the desired weight and take a seat.;Sit down and position your feet on the sled with a shoulder width stance.;Take a deep breath, extend your legs, and unlock the safeties.;Lower the weight under control until the legs are roughly 45 degrees or slightly below.;Drive the weight back to the starting position by extending the knees but don’t forcefully lockout.;Repeat for the desired number of repetitions.'),
							('03', 'Leg Extension', 'https://www.youtube.com/embed/0fl1RRgJ83I', 'The seated leg extension is an isolation exercise and one used to target the muscles of the quads.;This exercise can be particularly hard on the knees. So, for those with prior knee issues, it may be beneficial to stick with other movements, preferably compound, to target your quads.;The leg extension is a great exercise for quad development and may be beneficial to include in your workout routines if your goals are more aesthetics-driven.;The leg extension can be utilized in both leg workouts and full body workouts.'
																							   , 'Select the desired resistance on the weight stack and insert the pin.;Adjust the seat so that the knees are directly in line with the axis of the machine.;Sit down and position your shins behind the pad at the base of the machine.;Take a deep breath and extend your legs as you flex your quadriceps.;As you lock out the knees, exhale to complete the repetition.;Slowly lower your feet back to the starting position and repeat for the desired number of repetitions.'),
							('04', 'Leg Press Calf Raise', 'https://www.youtube.com/embed/RcKQbiL-ZOc', 'The leg press calf raise is a variation of the machine calf raise and an exercise used to build the muscles of the calves.;The calves can be a very stubborn muscle group, so it’s important to target them with plenty of different angles and a with a high training frequency.;This exercise can be incorporated into your leg days or full body days.'
																									  , 'Load the machine with the desired weight and take a seat.;Sit down and position your feet on the sled with a shoulder width stance.;Take a deep breath, extend your legs, but keep the safeties locked (if possible).;Position your feet at the base of the platform and allow the heels to hang off.;Lower the heels by dorsiflexing the ankles until the calves are fully stretched.;Drive the weight back to the starting position by extending the ankles and flexing the calves.;Repeat for the desired number of repetitions.'),
							('05', 'Stiff Leg Deadlift', 'https://www.youtube.com/embed/CkrqLaDGvOA', 'The stiff leg deadlift is a variation of the deadlift and an exercise used primarily to target the muscles of the hamstrings.;The stiff leg deadlift has long been thought of as the “leg” deadlift variation, despite all hip hinge movements primarily targeting the hamstrings. A smart option, to increase training frequency and work on the movement pattern, would be to perform stiff legs on your leg day and another deadlift variation on your back or pull days.;The hip hinge is a crucial movement pattern, so it is important to find a variation that is comfortable for you to perform (if able), and work on it.;The stiff leg deadlift is best utilized during your leg workouts and/or full body workouts.'
																									, 'Position the bar over the top of your shoelaces and assume a hip width stance.;Push your hips back and hinge forward until your torso is nearly parallel with the floor.;Reach down and grasp the bar using a shoulder width, double overhand grip.;Ensure your spine is neutral, shin is vertical, and your hips are roughly the same height as your shoulders.;Drive through the whole foot and focus on pushing the floor away.;Ensure the bar tracks in a straight line as you extend the knees and hips.;Once you have locked out the hips, reverse the movement by pushing the hips back and hinging forward.;Return the bar to the floor, reset, and repeat for the desired number of repetitions.'),
							('06', 'Seated Calf Raise', 'https://www.youtube.com/embed/Yh5TXz99xwY', 'The seated calf raise is a variation of the machine calf raise and an exercise used to isolate the muscles of the calves.;The calves can be a stubborn muscle group for a lot of people, so it’s important to experiment with several different angles when performing calf raises. You may also want to consider training the calves with a high training frequency.;The seated calf raise can be incorporated into your leg workouts and full body workouts.'
																								   , 'Take a seat on the machine and place the balls of your feet on the platform with your toes pointed forward - your heels will naturally hang off. Position the base of quads under the knee pad and allow your hands to rest on top.;Extend your ankles and release the safety bar.;Lower the heels by dorsiflexing the ankles until the calves are fully stretched.;Extend the ankles and exhale as you flex the calves.;Repeat for the assigned number of repetitions.'),
							('07', 'Incline Bench Press', 'https://www.youtube.com/embed/uIzbJX5EVIY', 'The incline bench press is a variation of the bench press and an exercise used to build the muscles of the chest. The shoulders and triceps will be indirectly involved as well.;Utilizing an incline will allow you to better target the upper portion of the chest, a lagging part for a lot of lifters.;You can include incline bench press in your chest workouts, upper body workouts, push workouts, and full body workouts.'
																									 , 'Lie flat on an incline bench and set your hands just outside of shoulder width.;Set your shoulder blades by pinching them together and driving them into the bench.;Take a deep breath and allow your spotter to help you with the lift off in order to maintain tightness through your upper back.;Let the weight settle and ensure your upper back remains tight after lift off.;Inhale and allow the bar to descend slowly by unlocking the elbows.;Lower the bar in a straight line to the base of the sternum (breastbone) and touch the chest.;Push the bar back up in a straight line by pressing yourself into the bench, driving your feet into the floor for leg drive, and extending the elbows.;Repeat for the desired number of repetitions.'),
							('08', 'One Arm Dumbbell Row', 'https://www.youtube.com/embed/YZgVEy6cmaY', 'The one arm dumbbell row is a variation of the dumbbell row and an exercise used to build back muscle and strength.;The back is a muscle group that requires a fair amount of variation. So, experiment with several different angles and hand positions to maximize your back muscle growth.;Rows are a foundational movement pattern and are very important to train for balanced muscle growth and strength. So, experiment until you find a rowing variation that you enjoy and work on it.;The one arm dumbbell row can be performed during your back workouts, upper body workouts, pull workouts, and full body workouts.'
																									  , 'Assume a standing position while holding a dumbbell in one hand with a neutral grip.;Hinge forward until your torso is roughly parallel with the floor (or slightly above) and then begin the movement by driving the elbow behind the body while retracting the shoulder blade.;Pull the dumbbell towards your body until the elbow is at (or just past) the midline and then slowly lower the dumbbell back to the starting position under control.;Repeat for the desired number of repetitions on both sides.'),
							('09', 'Seated Barbell Press', 'https://www.youtube.com/embed/Gxhx7GpRb5g', 'The seated barbell shoulder press is a variation of the overhead press and an exercise used to build shoulder strength and muscle.;Vertical press variations, such as the seated barbell shoulder press, are crucial movement patterns to train and should be incorporated into your workout routines. So, experiment with the variations until you find one that feels comfortable for you to perform and continue to work on it.;The seated barbell shoulder press can be included in your shoulder workouts, push workouts, upper body workouts, and full body workouts.'
																									  , 'Adjust the barbell to just below shoulder height while standing then load the desired weight onto the bar.;Place an adjustable bench beneath the bar in an upright position.;Sit down on the bench and unrack the bar using a pronated grip.;Inhale, brace, tuck the chin, then lower the bar to the top of your chest.;Exhale and press the bar back to lockout.;Repeat for the desired number of repetitions.'),
							('10', 'Pull Ups', 'https://www.youtube.com/embed/5oxviYmdHCY', 'The wide grip pull up is a variation of the pull up and an exercise used to target the upper back muscles such as the latissimus dorsi.;Vertical pulling movements, such as the wide grip pull up, are foundational movements that should be included in your workout routines. So, once you’ve found a variation you like and feels comfortable to you, master it as it will benefit you from a strength and aesthetic standpoint.;The wide grip pull up can be incorporated into back workouts, pull workouts, upper body workouts, or full body workouts.'
																						  , 'Using a pronated grip, grasp the pull bar with a wider than shoulder width grip.;Take a deep breath, squeeze your glutes and brace your abs. Depress the shoulder blades and then drive the elbows straight down to the floor while activating the lats.;Pull your chin towards the bar until the lats are fully contracted, then slowly lower yourself back to the start position and repeat for the assigned number of repetitions.'),
							('11', 'Skullcrushers', 'https://www.youtube.com/embed/K6MSN4hCDM4', 'The EZ bar skullcrusher is a variation of the skullcrusher and an exercise used to strengthen the muscles of the triceps.;The triceps can be trained in many different ways to promote growth and overhead extensions, such as the EZ bar skullcrusher, are an effective way to target the long head of the tricep.;Having bigger and stronger triceps are not only important from an aesthetic standpoint but can also help contribute to better performance on pressing motions such as the bench press.'
																							   , 'Select your desired weight and sit on the edge of a flat bench.;To get into position, lay back and keep the bar close to your chest. Once you are supine, press the weight to lockout.;Lower the weights towards your head by unlocking the elbows and allowing the ez bar to drop toward your forehead or just above.;Once your forearms reach parallel or just below, reverse the movement by extending the elbows while flexing the triceps to lockout the weight.;Repeat for the desired number of repetitions.'),
							('12', 'Dumbbell Bench Press', 'https://www.youtube.com/embed/dGqI0Z5ul4k', 'The dumbbell bench press is a variation of the barbell bench press and an exercise used to build the muscles of the chest.;Often times, the dumbbell bench press is recommended after reaching a certain point of strength on the barbell bench press to avoid pec and shoulder injuries.;Additionally, the dumbbell bench press provides an ego check in the amount of weight used due to the need to maintain shoulder stability throughout the exercise.;The exercise itself can be featured as a main lift in your workouts or an accessory lift to the bench press depending on your goals.'
																									  , 'Pick up the dumbbells off the floor using a neutral grip (palms facing in). Position the ends of the dumbbells in your hip crease, and sit down on the bench.;To get into position, lay back and keep the weights close to your chest. Once you are in position, take a deep breath, and press the dumbbells to lockout at the top.;Slowly lower the dumbbells under control as far as comfortably possible (the handles should be about level with your chest).;Contract the chest and push the dumbbells back up to the starting position.;Repeat for the desired number of repetitions.')
    ''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS Dish (
    Id TEXT NOT NULL PRIMARY KEY,
    Name TEXT,
    Image BLOB,
    Nutrition TEXT,
    Recipe TEXT,
    Steps TEXT
    )
    ''')
    dish_data = [
        ('01', 'Gluten-Free Pancakes', read_image('D:/synaptifit/streamlit/images/dishes/01.jpg'), '176;26;6;8',
         'Cream cheese:0.5 oz;Egg:1 fruit;Honey: 1 teaspoon;Cinnamon: 1/2 teaspoon;Oatmeal: 1/2 cup',
         'Blend ingredients...'),
        ('02', 'Microwave Poached Eggs', read_image('D:/synaptifit/streamlit/images/dishes/02.jpg'), '72;0;5;6',
         'Egg:1 fruit;Vinegar: 1/8 teaspoon;Water: 1/3 cup', 'Add the water and white vinegar...'),
        ('03', 'Tuna and Hummus', read_image('D:/synaptifit/streamlit/images/dishes/03.jpg'), '86.5;2.5;2;15',
         'Tuna: 2.5 oz;Rosemary: 1/2 teaspoon;Pepper: 0.1 g;Hummus: 1 tablespoon',
         'Mix all ingredients together and serve.'),
        (
        '04', 'Carrots', read_image('D:/synaptifit/streamlit/images/dishes/04.jpg'), '86;20;0;2', 'Baby carrots: 246 g',
        'Enjoy by themselves. Optionally, enjoy with a side of hummus (there are other carrot + dip recipes on ETM you can swap in).'),
        ('05', '6 Minute Salmon', read_image('D:/synaptifit/streamlit/images/dishes/05.jpg'), '257;7;10;37',
         'Sockeye salmon: 6 oz;Salt: 0.1 g;Garlic powder: 1/2 teaspoon;Lemons: 1/2 fruit',
         'Preheat a cast iron skillet to high heat and set your oven to the broiler setting;Take the filet of salmon and pat dry with a paper towel. Salt the skin side of the salmon and add it to the pan, skin side down. Set the timer for two minutes. While the skin side is searing, season the other side generously with the garlic powder.Once the salmon is seared, place the cast iron into the oven for 4 minutes under the broiler;Once the 4 minutes are up, serve the salmon with lemon wedges;Enjoy!'),
        ('06', 'Green Kale Salad', read_image('D:/synaptifit/streamlit/images/dishes/06.jpg'), '72;10;2;4',
         'Kale: 44.8 g;Olive oil: 1/2 teaspoon;Garlic: 0.5 g;Salt: 0.8 g;Pepper: 0.35 g;Celery: 22 g;Green bell pepper: 26 g;Zucchini: 16 g;Cucumber: 17 g;Broccoli: 12 g;Peas: 2 tablespoon;Alfalfa sprouts: 2 tablespoon',
         'Microwave peas until just defrosted set aside. Chop and prep other vegetables. Add kale, olive oil, garlic, salt and black pepper to a large bowl. Mix kale and olive oil together well so that kale is fully coated;Add remaining ingredients to the bowl and mix. Serve.'),
        ('07', 'Cream Cheese Omelet', read_image('D:/synaptifit/streamlit/images/dishes/07.jpg'), '295;1;27;12',
         'Olive oil: 1 tablespoon;Egg: 2 fruit;Salt: 0.4 g;Pepper: 0.1 g;Cream cheese: 1 tablespoon',
         'Heat 1 tbsp oil in a non-stick skillet over medium heat;Whisk together eggs, salt, and pepper in a small bowl;Once pan is hot and nicely coated, pour eggs into pan and cover base. Allow to cook until eggs begin to look dry; redistributing egg mixture as needed;Fold 1/3 of the egg toward the middle. Repeat with opposite side of egg, folding another 1/3 toward the middle;Slide onto plate seam side down;Top with a dollop of cream cheese and enjoy!'),
        ('08', 'Strawberries', read_image('D:/synaptifit/streamlit/images/dishes/08.jpg'), '46;11;0;1',
         'Strawberries: 144 g', 'Wash and eat.'),
        ('09', 'Cottage Cheese and Black Bean Tuna Salad', read_image('D:/synaptifit/streamlit/images/dishes/09.jpg'),
         '171;8;2;31', 'Tuna: 4 oz;Cottage cheese: 56 g;Celery: 20 g;Canned black beans: 2 tablespoon',
         'Mix all ingredients together well in a bowl. Serve as desired and enjoy!'),
        ('10', 'Spinach Tomato Salad', read_image('D:/synaptifit/streamlit/images/dishes/10.jpg'), '186;13;14;6',
         'Spinach: 150 g;Scallions: 50 g;Tomatoes: 62 g;Olive oil: 1 tablespoon;Pepper: 0.1 g;Lemon juice: 1/2 fruit',
         'Wash spinach well, drain, and chop. Squeeze out excess water. Chop green onions and tomato;Put spinach in a mixing bowl and add the tomato, scallions, oil, pepper, and the juice from 1 squeezed lemon. Toss and serve.'),
        ('11', 'Pasta with Red Sauce and Mozzarella', read_image('D:/synaptifit/streamlit/images/dishes/11.jpg'),
         '309;48;7;16', 'Whole wheat pasta: 140 g;Pasta sauce: 130 g;Mozzarella cheese: 1 oz',
         'Prepare pasta as per package directions, drain;Put pasta in bowl, drizzle pasta sauce on top, mix in, put shredded mozzarella cheese on top, and heat in microwave for 2 minutes. Enjoy!'),
        ('12', 'Blackberry Chocolate Shake', read_image('D:/synaptifit/streamlit/images/dishes/12.jpg'), '214;17;17;2',
         'Ice cubes: 7 piece;Blackberries: 38 g;Cocoa: 1 tablespoon;Stevia Sweetener: 0.3 g;Coconut oil: 1 tablespoon;Almond milk: 240 g',
         'Combine all ingredients in a blender and pulse until smooth. Enjoy!'),
        ('13', 'Oranges', read_image('D:/synaptifit/streamlit/images/dishes/13.jpg'), '62;15;0;1', 'Oranges: 1 fruit',
         'Peel or slice orange and eat.'),
        (
        '14', 'Curried Cabbage and Carrot Slaw', read_image('D:/synaptifit/streamlit/images/dishes/14.jpg'), '61;9;0;6',
        'Onions: 18 g;Spearmint: 2 g;Carrots: 36 g;Nonfat greek yogurt: 47 g;Curry powder: 1/2 teaspoon;Lemon juice: 1/4 teaspoon;Cabbage: 24 g;Salt: 0.067 g;Pepper: 0.02 g',
        'Chop onion. Chop fresh mint. Peel and coarsely grate carrots;Combine all ingredients (excluding salt and pepper) in a bowl, toss together well. Season with salt and pepper to taste. Enjoy!'),
        ('15', 'Fresh Jicama Salad', read_image('D:/synaptifit/streamlit/images/dishes/15.jpg'), '76;18;0;2',
         'Yambean (jicama): 180 g;Chili powder: 1/2 teaspoon;Lime juice: 1 tablespoon;Fresh cilantro: 1 g;Salt: 3g',
         'Cut jicama into sticks. Toss with lime juice, chili powder, salt, and chopped cilantro. Enjoy!'),
        ('16', 'Cinnamon Roll Smoothie', read_image('D:/synaptifit/streamlit/images/dishes/16.jpg'), '303;34;14;12',
         'Almond milk: 120 g;Greek yogurt: 120 g;Rolled oats: 10 g;Brown sugar: 1/2 tablespoon;Cinnamon: 1/8 teaspoon;Banana: 1/2 fruit',
         'Combine all ingredients in a blender and pulse until smooth. Enjoy!'),
        ('17', 'Buttered Toast', read_image('D:/synaptifit/streamlit/images/dishes/17.jpg'), '121;12;7;4',
         'Whole-wheat bread: 1 slices;Butter: 1/2 tablespoon',
         'Toast bread to desired doneness;Spread butter across until evenly distributed;Enjoy!'),
        ('18', 'Sun-Dried Tomato Turkey Roll-up', read_image('D:/synaptifit/streamlit/images/dishes/18.jpg'),
         '330;36;15;15',
         'Sun-dried tomatoes: 5 miếng;Tortillas: 1 bánh;Cream cheese: 2 tablespoon;Deli cut turkey: 57 g;Spinach: 30 g',
         'Chop sun-dried tomatoes into thin strips;Spread cream cheese on tortilla, then place turkey, spinach and sun-dried tomatoes inside. Roll up, cut in half, and enjoy!'),
        ('19', 'Roasted Salmon', read_image('D:/synaptifit/streamlit/images/dishes/19.jpg'), '242;0;14;28',
         'Atlantic salmon: 142 g;Olive oil: 1 teaspoon;Tarragon: 0.3 g;Chives: 1.5 g',
         'PREPARATION: Chop chives;Preheat oven to 425°F;Rub salmon all over with 1 teaspoon oil and season with salt and pepper. Roast, skin side down, on a foil-lined baking sheet in upper third of oven until fish is just cooked through, about 12 minutes. Cut salmon in half crosswise, then lift flesh from skin with a metal spatula and transfer to a plate. Discard skin, then drizzle salmon with oil and sprinkle with herbs.'),
        ('20', 'Veggie Omelet', read_image('D:/synaptifit/streamlit/images/dishes/20.jpg'), '149;11;1;24',
         'Spinach: 30 g;Salt: 0.4 g;Pepper: 0.1 g;Onions: 40 g;Red bell pepper: 40 g;Mushrooms: 70 g;Egg white: 180 g;Almond milk: 1 tablespoon',
         'Clean the spinach off and place it into a pan while still wet. Cook on medium heat and season with salt and pepper;Once the spinach is wilted (2-3 minutes), add the onion, bell pepper, and mushroom, and cook until the onions are translucent, the pepper chunks are soft, and mushrooms are tender;Whisk the egg whites with the almond milk;Add the eggs to the pan and scramble until cooked. Top with salt and pepper. Enjoy!'),
        ('21', 'Tuna Poke', read_image('D:/synaptifit/streamlit/images/dishes/21.jpg'), '164;1;4;29',
         'Tuna: 4 oz;Sesame seeds: 1 teaspoon;Sesame oil: 1/2 teaspoon;Soy sauce: 1 teaspoon;Stevia Sweetener: 0.5 g;Salt: 0.2 g',
         'Cut fish into cubes. Toss all ingredients and enjoy!'),
        ('22', 'Green salad', read_image('D:/synaptifit/streamlit/images/dishes/22.jpg'), '70;1;7;1',
         'Lettuce: 23 g;Spinach: 8 g;Arugula: 5 g;Basil: 1.5 g;Olive oil: 1/2 tablespoon;Red wine vinegar: 1/2 tablespoon;Salt: 0.1 g;Pepper: 0.025 g;Dijon mustard: 1/4 teaspoon',
         'Any 4 cups of greens should be fine. In a serving bowl, combine the greens and basil;To make the dressing, place all ingredients in a screw-top jar and shake well to combine. Just before serving, pour dressing evenly over the leaves and gently toss.'),
        ('23', 'Thai Pork Salad', read_image('D:/synaptifit/streamlit/images/dishes/23.jpg'), '399;9;24;35',
         'Pork shoulder, blade: 127 g;Oyster sauce: 3/4 tablespoon;Soy sauce: 3/4 tablespoon;Lettuce: 35 g;Carrots: 15 g;Red bell pepper: 60 g;Light mayonnaise: 3/4 tablespoon',
         'Mix the pork with the oyster and soy sauce in a mixing bowl, and marinade overnight if desired;Fry the pork in a saucepan over a high heat, cooking in 2 portions if necessary - making sure not to overcrowd the pan;Combine all ingredients in a salad bowl (or Tupperware container if storing for later);This recipe can easily be doubled or halved by frying up the meat first and storing in the refrigerator or freezer until ready to eat.'),
        ('24', 'Orange Breakfast Fruit Smoothie', read_image('D:/synaptifit/streamlit/images/dishes/24.jpg'),
         '371;59;2;34',
         'Strawberries: 150 g;Banana: 1 fruit;Oranges: 1 fruit;Whey protein powder: 30 g;Nonfat greek yogurt: 4 tablespoon',
         'Combine all ingredients in a blender and pulse until smooth. Enjoy!'),
        ('25', 'Tomato and Cheese Wrap', read_image('D:/synaptifit/streamlit/images/dishes/25.jpg'), '302;29;16;11',
         'Tortillas: 1 bánh;Mayonnaise-like dressing: 1 tablespoon;Tomatoes: 60 g;Lettuce: 36 g;Cheddar cheese: 1 oz',
         'Lightly spread mayo on tortilla shell;Cut tomatoes however you like them;Layer ingredients, spreading them over the tortilla;Tuck up about an inch the side of the shell you''ve decided is the bottom and roll up wrap. Enjoy!'),
        ('26', 'Yogurt with Papaya', read_image('D:/synaptifit/streamlit/images/dishes/26.jpg'), '194;23;1;24',
         'Nonfat greek yogurt: 8 oz;Papayas: 140 g', 'Peel and seed papaya and slice. Mix into yogurt and enjoy!'),
        ('27', 'Vietnamese Tofu and Noodle Salad', read_image('D:/synaptifit/streamlit/images/dishes/27.jpg'),
         '321;29;19;12',
         'Sunflower oil: 1/2 tablespoon;Tofu: 63 g;Rice noodles: 14 g;Rice wine vinegar: 1 tablespoon;Sugar: 1 teaspoon;Red peppers: 11 g;Carrots: 30 g;Cucumber: 26 g;Red bell pepper: 23 g;Scallions: 11 g;Peppermint: 1 g;Basil: 1.5 g;Lettuce: 2 g;Peanuts: 18 g',
         'Soak rice noodles in lukewarm water until tender. Drain. Heat the oil in a medium-sized frying pan over a medium heat and fry the tofu for 8–10 minutes, turning regularly, until golden and crisp. Drain on kitchen paper;Add the noodles to the pan, with a splash of water and heat until warmed and cooked through;Meanwhile, mix together the ingredients for the dressing (rice vinegar, sugar, chopped red peppers), set aside;Combine the noodles, carrots, cucumber, cabbage, red pepper, spring onions, and half the herbs in a bowl, spoon the dressing over and mix together;Arrange the Little Gem lettuce leaves on a large, flat serving plate and top with the noodle salad, tofu, remaining herbs and peanuts before serving.'),
        ('28', 'Sea Salt Edamame', read_image('D:/synaptifit/streamlit/images/dishes/28.jpg'), '147;11;7;13',
         'Salt: 0.4 g;Soybeans: 100 g',
         'Cook edamame in microwave, about 2 minutes;Sprinkle salt over;Just eat the beans, not the pods.'),
        (
        '29', 'Egg White and Mushroom Omelet', read_image('D:/synaptifit/streamlit/images/dishes/29.jpg'), '142;5;6;17',
        'Egg white: 130 g;Whole milk: 2 tablespoon;Salt: 0.4 g;Pepper: 0.1 g;Olive oil: 1 teaspoon;Mushrooms: 70 g',
        'Whisk the egg whites, milk, salt, and pepper in a medium bowl until thoroughly combined. Set a serving plate aside;Heat oil in an 8-inch nonstick frying pan over medium heat until foaming. Add mushrooms to the pan and cook until tender, about 5-10 minutes. Remove frmo pan. Add the egg mixture to the pan and stir constantly with a rubber spatula, moving the eggs around the pan until they form small curds, about 2 to 3 minutes;Gently shake the pan and use the spatula to spread the egg mixture evenly across the pan;Remove the pan from heat. Top eggs with the mushrooms. Using the spatula, fold a third of the omelet over and onto itself. Gently push the folded side of the omelet toward the edge of the pan;Tilt the pan over the serving plate and roll the omelet onto the plate, seam side down. Serve;Enjoy!'),
        ('30', 'Turkey Wrap', read_image('D:/synaptifit/streamlit/images/dishes/30.jpg'), '391;29;22;20',
         'Tortillas: 1 bánh;Sliced turkey: 58 g;Lettuce: 56 g;Avocados: 68 g;Tomatoes: 62 g;sliced cheese: 2 slices;Hummus: 1 tablespoon',
         'Slather hummus onto tortilla;Layer with turkey, lettuce, avocado, tomato, and cheese;Roll up and enjoy!'),
        ('31', 'Shrimp Cakes', read_image('D:/synaptifit/streamlit/images/dishes/31.jpg'), '110;5;4;12',
         'Shrimp: 80 g;Scallions: 4 g;Red bell pepper: 6 g;Bread crumbs: 5 g;Egg Whites: 12 g;Olive oil: 1 teaspoon',
         'Purée about 5-6 medium shrimp, majority of scallions, and the bell pepper in a food processor. Chop remaining shrimp and mix together with purée, breadcrumbs, and egg whites. Form into 4 patties and refrigerate for about a hour;Heat oil in a pan over medium-high heat. Add patties and cook about 5 minutes per side until patties are cooked through and golden brown. Enjoy!'),
        ('32', 'Tuna Apple Salad', read_image('D:/synaptifit/streamlit/images/dishes/32.jpg'), '482;29;13;65',
         'Tuna: 330 g;Apples: 112 g;Pickle relish: 1 tablespoon;Mayonnaise-like dressing: 3 tablespoon;Garlic powder: 1 teaspoon',
         'Drain water from cans and place tuna in a bowl;Finely chop apple and add to bowl;Stir in sweet relish, mayonnaise, and garlic powder. Use as desired and enjoy!'),
        ('33', 'Basic Parmesan Egg White Omelet', read_image('D:/synaptifit/streamlit/images/dishes/33.jpg'),
         '228;4;15;18',
         'Egg white: 132 g;Reduced fat milk: 2 tablespoon;Salt: 0.4 g;Pepper: 0.1 g;Butter: 1 tablespoon;Parmesan cheese: 2 tablespoon',
         'Whisk the egg whites, cheese, milk, salt, and pepper in a medium bowl until thoroughly combined. Set a serving plate aside;Melt the butter in an 8-inch nonstick frying pan over medium heat until foaming. Add the egg mixture and stir constantly with a rubber spatula, moving the eggs around the pan until they form small curds, about 2 to 3 minutes;Gently shake the pan and use the spatula to spread the egg mixture evenly across the pan;Remove the pan from heat. Using the spatula, fold a third of the omelet over and onto itself. Gently push the folded side of the omelet toward the edge of the pan;Tilt the pan over the serving plate and roll the omelet onto the plate, seam side down. Serve.'),
        ('34', 'Turkey, Goat Cheese, and Avocado Roll', read_image('D:/synaptifit/streamlit/images/dishes/34.jpg'),
         '120;4;9;6',
         'Lettuce: 17 g;Deli cut turkey: 10 g;Goat cheese: 14 g;Walnuts: 8 g;Avocados: 8 g;Red bell pepper: 19 g',
         'Top each lettuce leaf with a turkey slice;Spread each turkey slice with 1 tablespoon goat cheese;Sprinkle 1 teaspoon walnuts on each roll and top with 1 slice avocado;Roll and garnish with chopped bell pepper, if desired.'),
        ('35', 'Chicken Soup', read_image('D:/synaptifit/streamlit/images/dishes/35.jpg'), '318;22;10;33',
         'Olive oil: 1/2 teaspoon;Onions: 75 g;Carrots: 46 g;Thyme: 0.6 g;Chicken stock: 180 g;Chicken breast: 75 g;Mushrooms: 50 g;Salt: 0.1 g;Pepper: 0.025 g;Greek yogurt: 2 tablespoon;Garlic: 0.75 g;Lemon juice: 1/2 teaspoon',
         'Spray a pan with non-stick spray and cook chicken for 8-10 minutes per side or until cooked through, no longer pink, and the juices run clear. Let rest 5 minutes before cutting into bite sized pieces;Heat oil in a large heavy-based pan over medium heat. Add onions, carrots, and thyme, then gently fry for 15 minutes. Stir in stock, bring to a boil, cover, then simmer for 10 minutes;Remove half the mixture, then purée with a stick blender (or in a regular blender). Tip back into the pan with the rest of the soup, mushrooms and salt and pepper, to taste. Add the chicken, then simmer for 5 minutes until heated through;Mix in the yogurt, garlic, and lemon juice, swirl into the soup in bowls, then serve.'),
        ('36', 'Salsa salad', read_image('D:/synaptifit/streamlit/images/dishes/36.jpg'), '187;37;2;10',
         'Lettuce: 140 g;Salsa: 65 g;Fresh cilantro: 5 g;Parsley: 8 g;Pinto beans: 120 g;Carrots: 30 g;Corn: 40 g',
         'Combine everything except the corn, beans and salsa and toss with the parsely and cilantro;Mix together the pinto beans, corn, salsa and top the salad'),
        ('37', 'Easy Steamed Green Beans', read_image('D:/synaptifit/streamlit/images/dishes/37.jpg'), '31;7;0;2',
         'Water: 60 g;Salt: 1.5 g;Green beans: 100 g',
         'Bring salted water to boil in a large frying pan or sauté pan;Add green beans, cover, and cook until green beans are tender to the bite and water has evaporated. Serve hot and enjoy!'),
        (
            '38', 'Peanut Butter Banana Oatmeal', read_image('D:/synaptifit/streamlit/images/dishes/38.jpg'),
            '309;47;11;11',
            'Oatmeal: 40 g;Water: 276 g;Salt: 0.2 g;Peanut butter: 1 tablespoon;Banana: 1/2 fruit;Reduced fat milk: 3 tablespoon;Butter: 1/4 teaspoon',
            'Combine the oatmeal, water and salt in a medium saucepan. Bring to a boil;Cook for 5 minutes stirring occasionally. Add the peanut butter, banana, milk and butter and mix gently. Cook for another minute and serve.'),
        ('39', 'Tuna Avocado Salad', read_image('D:/synaptifit/streamlit/images/dishes/39.jpg'), '124;4;6;15',
         'Avocados: 34 g;Tuna: 74 g;Salt: 0.4 g;Pepper: 1.5 g',
         'Using a fork, mash up the tuna really well until the consistency is even;Mix in the avocado until smooth;Add salt and pepper to taste. Enjoy!'),
        (
            '40', 'Spicy Yogurt Dip with Carrots', read_image('D:/synaptifit/streamlit/images/dishes/40.jpg'),
            '120;16;1;13',
            'Pepper or hot sauce: 1 teaspoon;Carrots: 130 g;Nonfat greek yogurt: 4 oz',
            'Stir hot sauce into yogurt to combine. Enjoy with carrot strips.'),
        ('41', 'Simple Steak', read_image('D:/synaptifit/streamlit/images/dishes/41.jpg'), '293;0;15;38',
         'Beef tenderloin: 170 g;Salt: 1 teaspoon;Pepper: 1/4 teaspoon;Olive oil: 1 teaspoon',
         'Remove the steak from the refrigerator and let it come to room temperature, about 30 to 45 minutes;Season the steak on both sides with the salt and pepper. Rub both sides with the olive oil and set aside;Heat a medium heavy-bottomed frying pan (not nonstick!) over high heat until very hot but not smoking, about 3 to 4 minutes. (If the pan gets too hot and starts to smoke, take it off the heat to cool a bit.) Place the steak in the pan and let it cook undisturbed until a dark crust forms on the bottom, about 3 to 4 minutes;Flip the steak using tongs or a spatula and cook until it''s medium rare, about 3 to 4 minutes more. To check for doneness, use your finger to press on the steak: It should be firm around the edges but still give in the center. You can also use an instant-read thermometer, it should read about 125°F to 130°F;Transfer the steak to a cutting board and let it rest for at least 5 minutes before serving.'),
        ('42', 'Mediterranean Salad', read_image('D:/synaptifit/streamlit/images/dishes/42.jpg'), '74;18;0;2',
         'Spinach: 15 g;Pickles: 7.5 g;Mangos: 41 g;Cherry tomatoes: 50 g;Onions: 55 g;Lemon juice: 3 g;Salt: 0.2 g;Pepper: 0.05 g;Garlic powder: 1/2 teaspoon',
         'Chop and assemble all the ingredients. Toss with your favorite dressing and enjoy!'),
        ('43', 'Cottage Cheese & Applesauce', read_image('D:/synaptifit/streamlit/images/dishes/43.jpg'), '214;20;2;28',
         'Applesauce: 120 g;Cottage cheese: 225 g', 'Mix together and enjoy!'),
        ('44', 'Turkey Salad', read_image('D:/synaptifit/streamlit/images/dishes/44.jpg'), '276;4;9;42',
         'Turkey, dark meat: 140 g;Lettuce: 47 g;Mayonnaise-like dressing: 1 tablespoon;Table Blend Salt Free Seasoning Blend: 1 g;Salt: 0.4 g;Pepper: 0.1 g;Lemon juice: 1 teaspoon',
         'Put seasonings, lemon juice, turkey, and mayo in a bowl. Mix well. Serve on top of lettuce.'),
        ('45', 'Cinnamon Yogurt with Sliced Apple', read_image('D:/synaptifit/streamlit/images/dishes/45.jpg'),
         '165;35;1;8', 'Apples: 1 fruit;Nonfat yogurt: 120 g;Cinnamon: 1/4 teaspoon',
         'Slice apple;Sprinkle cinnamon on yogurt, dip slices of apple into yogurt and enjoy!'),
        ('46', 'Greek Spaghetti', read_image('D:/synaptifit/streamlit/images/dishes/46.jpg'), '687;86;27;25',
         'Butter: 1 1/2 teaspoon;Spaghetti: 4 oz;Salt: 0.75 g;Oregano: 1/4 teaspoon;Parmesan cheese: 25 g',
         'Preheat oven to 250 degrees F (120 degrees C);Bring a large pot of lightly salted water to a boil. Add pasta and cook for 8 to 10 minutes or until al dente, drain;In a medium skillet over medium heat, melt butter with salt and cook until just brown. Remove from heat and toss with pasta, cheese and oregano. Pour into a 7x11 inch baking dish;Bake in preheated oven 10 to 15 minutes, until hot and bubbly.'),
        ('47', 'Spinach and Poached Egg Muffins', read_image('D:/synaptifit/streamlit/images/dishes/47.jpg'),
         '375;38;15;25',
         'Vinegar: 2 tablespoon;English muffins: 1 bánh;Spinach: 195 g;Nutmeg: 1 teaspoon;Sour cream: 2 tablespoon;Egg: 2 fruit;Salt: 0.4 g;Pepper: 0.1 g',
         'Put a pan of water on to boil and add the vinegar;Toast the muffin halves until lightly browned. Meanwhile, heat the spinach through on a saucepan, just a few minutes, season to taste and add some freshly ground nutmeg and the sour cream;When the water is at a simmer, break the eggs into a small cup and then carefully slide them into the water. Turn the heat down and simmer for 3 minutes until the white has set and it''s firm, but the yolks are still soft and runny;Remove the eggs from the water with a slotted spoon. Spoon the warm, cooked spinach on top of the muffin halves and then put the eggs on top of the spinach. Season with salt and freshly ground black pepper and serve straight away.'),
        ('48', 'Whole Wheat Toast', read_image('D:/synaptifit/streamlit/images/dishes/48.jpg'), '71;12;1;3',
         'Whole-wheat bread: 1 slices',
         'Put a slice of whole wheat bread into the toaster. Eat by itself or as a side.'),
        ('49', 'Cucumber Apple Salad', read_image('D:/synaptifit/streamlit/images/dishes/49.jpg'), '98;24;1;2',
         'Apples: 1/2 fruit;Cucumber: 1 fruit;Vinegar: 1 tablespoon;Water: 1 tablespoon;Garlic Salt: 1/2 teaspoon;Pepper: 0.1 g;Stevia Sweetener: 1 g',
         'Chop apple and thinly slice cucumber. Combine vinegar and water. Season with garlic salt, pepper, and stevia to taste. Enjoy!'),
        ('50', 'Broccoli Potato Soup', read_image('D:/synaptifit/streamlit/images/dishes/50.jpg'), '184;34;4;7',
         'Olive oil: 3/4 teaspoon;Leeks: 22 g;Carrots: 30 g;Potato: 92 g;Garlic: 4 g;Salt: 1/4 teaspoon;Broccoli: 150 g',
         'Cut the leek and fry in oil in a skillet over medium heat;After few minutes add chopped carrots, potato, and salt;Add hot water to cover and bring to a boil. Cook until potatoes are fork tender;Add chopped garlic and broccoli;Boil for few minutes until broccoli is tender;Transfer mixture to a blender or use a stick blender to pulse until smooth. Serve hot and enjoy!'),
        ('51', 'Cinnamon Toast', read_image('D:/synaptifit/streamlit/images/dishes/51.jpg'), '130;19;5;4',
         'Whole-wheat bread: 1 slices;Butter: 1 teaspoon;Sugar: 1/2 tablespoon;Cinnamon: 1/4 teaspoon',
         'Use a toaster to toast the bread to desired darkness. Spread butter or margarine onto one side of each slice. In a cup or small bowl, stir together the sugar and cinnamon, sprinkle generously over hot buttered toast.'),
        (
        '52', 'Yogurt with Almonds & Honey', read_image('D:/synaptifit/streamlit/images/dishes/52.jpg'), '259;18;10;27',
        'Nonfat greek yogurt: 8 oz;Almonds: 18 g;Honey: 1 teaspoon',
        'Rough-chop almonds and mix into yogurt and honey. Enjoy!'),
        ('53', 'Stuffed Sweet Potato with Hummus', read_image('D:/synaptifit/streamlit/images/dishes/53.jpg'),
         '364;64;6;15', 'Sweet potato: 1 củ;Kale: 50 g;Canned black beans: 130 g;Hummus: 62 g;Water: 2 tablespoon',
         'Prick sweet potato all over with a fork. Microwave on high until cooked through, 7 to 10 minutes;Meanwhile, wash kale and drain. Place in a medium saucepan, cover and cook over medium-high heat, stirring once or twice, until wilted. Add beans and water. Continue cooking, uncovered, stirring occasionally, until the mixture is steaming hot, 1 to 2 minutes;Split the sweet potato open and top with the kale and bean mixture. Top with hummus.'),
        ('54', 'Mango Smoothie', read_image('D:/synaptifit/streamlit/images/dishes/54.jpg'), '170;40;1;3',
         'Mangos: 1 fruit;Coconut water: 240 g;Ice cubes: 1 piece',
         'Combine all ingredients in a blender and pulse until smooth. Enjoy!'),
        ('55', 'Yogurt & Cantaloupe', read_image('D:/synaptifit/streamlit/images/dishes/55.jpg'), '188;21;1;24',
         'Nonfat greek yogurt: 8 oz;Melons: 160 g', 'Cut cantaloupe into pieces and mix with yogurt. Enjoy!'),
        ('56', 'Monte Cristo sandwich', read_image('D:/synaptifit/streamlit/images/dishes/56.jpg'), '551;30;31;36',
         'Sliced ham: 3 slices;Swiss cheese: 1 oz;Egg: 1 fruit;Reduced fat milk: 1 1/3 tablespoon;Butter: 3/4 tablespoon;Whole-wheat bread: 2 slices',
         'For each sandwich, place about 2 slices ham and 1 slice Swiss cheese between 2 slices of bread. In a mixing bowl whisk together the eggs and milk;Dip sandwiches in the egg mixture, turning carefully, until well coated and all of the mixture is absorbed. Melt butter in a large skillet or on griddle;When skillet is hot and butter is bubbly, place sandwiches in skillet and cook slowly for 8-10 minutes, turn and continue cooking until cheese is melted and both sides are golden brown.'),
        ('57', 'Nonfat greek yogurt', read_image('D:/synaptifit/streamlit/images/dishes/57.jpg'), '142;9;1;24',
         'Nonfat greek yogurt: 240 g',
         'Scoop yogurt into a cup or bowl. To sweeten, try adding a sugar-free sweetener or a tiny bit of honey and stir.'),
        ('58', 'Broccoli and Apple Salad', read_image('D:/synaptifit/streamlit/images/dishes/58.jpg'), '55;9;2;1',
         'Vinegar: 10 g;Sugar: 1 teaspoon;Dijon mustard: 3/4 teaspoon;Canola oil: 1/2 teaspoon;Pepper: 0.1 g;Salt: 0.2 g;Broccoli: 23 g;Apples: 20 g;Onions: 5 g',
         'Combine vinegar, sugar, dijon mustard, canola oil, salad and pepper in a large bowl. Stir well with a whisk;Add apple, broccoli and onion to mixture, and toss to coat.'),
        (
        '59', 'Cottage Cheese with Dill Tuna', read_image('D:/synaptifit/streamlit/images/dishes/59.jpg'), '223;3;3;46',
        'Cottage cheese: 113 g;Dill: 1/2 teaspoon;Tuna: 165 g',
        'Drain tuna. Mix in bowl with cottage cheese and dill. Enjoy!'),
        ('60', 'Carrot and Orange Juice', read_image('D:/synaptifit/streamlit/images/dishes/60.jpg'), '81;19;0;2',
         'Carrots: 2 củ;Oranges: 1/2 fruit',
         'Peel orange. Juice carrots and orange. Mix together well just before serving. Enjoy!'),
        ('61', 'Tomato Basil Pasta', read_image('D:/synaptifit/streamlit/images/dishes/61.jpg'), '277;47;8;10',
         'Whole wheat pasta: 2 oz;Tomatoes: 90 g;Spinach: 15 g;Pepper: 1/8 teaspoon;Salt: 1/4 teaspoon;Basil: 1 lá;Olive oil: 1/2 tablespoon',
         'Start water boiling;In second pot add tomato (diced/chopped), basil leaves, spinach (chopped), salt, pepper, and olive oil and put on medium heat for 10 minutes. Stir occasionally;Boil pasta (I prefer rotini) for ~8 minutes (follow directions on box). Then drain;Mix cooked pasta with sauce mixture.'),
        ('62', 'Strawberry Mango Shake', read_image('D:/synaptifit/streamlit/images/dishes/62.jpg'), '152;24;4;7',
         'Reduced fat milk: 180 g;Mangos: 41 g;Strawberries: 36 g;Sugar: 1/2 tablespoon',
         'Blend milk, mangos, strawberries, and sugar together well. Enjoy!'),
        ('63', 'Yogurt Artichoke Dip with Rye Crisps', read_image('D:/synaptifit/streamlit/images/dishes/63.jpg'),
         '169;26;1;15',
         'Artichoke Hearts, Quarters: 200 g;Dill weed: 1/2 teaspoon;Nonfat greek yogurt: 4 oz;Garlic: 3 g;Crispbread crackers: 20 g',
         'Chop drained artichoke hearts and mince garlic. Combine with dill and yogurt. Mix well. Serve with rye crackers. Enjoy!'),
        ('64', 'Mini Flatbread Pizza', read_image('D:/synaptifit/streamlit/images/dishes/64.jpg'), '158;22;5;9',
         'Pita bread: 1 bánh;Pizza sauce: 1 tablespoon;Basil (chopped): 2.5 g;Ricotta cheese: 1 tablespoon;Mozzarella cheese: 14 g;Cherry tomatoes: 37 g;Green bell pepper: 30 g;Onions: 10 g;Basil: 4 lá',
         'Preheat oven to 400 degrees F;Spread 1 tbsp pizza sauce on top of each pita. Sprinkle evenly with basil. Stir together cheeses, and dollop on pizza. Arrange tomatoes, peppers and onion evenly on top;Bake for 5 minutes, or until cheese melts and vegetables are tender. Garnish with basil leaves, if desired. Enjoy!'),
        ('65', 'Tofu Salad', read_image('D:/synaptifit/streamlit/images/dishes/65.jpg'), '207;10;16;8',
         'Lettuce: 94 g;Cherry tomatoes: 75 g;Tofu: 85 g;Olive oil: 1 tablespoon;Red Onion: 18 g',
         'Gently mix the ingredients in a bowl;Enjoy!'),
        ('66', 'Banana and Kale Smoothie', read_image('D:/synaptifit/streamlit/images/dishes/66.jpg'), '278;54;6;9',
         'Coconut water: 240 g;Banana: 75 g;Kale: 67 g;Chia seeds: 14 g;Blueberries: 111 g',
         'Combine all ingredients in a blender and pulse until smooth. Enjoy!'),
        ('67', 'Rice Cake with Strawberries and Honey', read_image('D:/synaptifit/streamlit/images/dishes/67.jpg'),
         '125;31;0;1', 'Strawberries: 83 g;Honey: 1 tablespoon;Rice cakes: 1 bánh',
         'Slice strawberries. Place on rice cake and drizzle with honey. Enjoy!'),
        ('68', 'Bologna Caesar Wraps', read_image('D:/synaptifit/streamlit/images/dishes/68.jpg'), '224;31;8;7',
         'Lettuce: 35 g;Parmesan cheese: 1 1/4 tablespoon;Caesar salad dressing: 2 tablespoon;Bologna Chicken/ pork: 7 g;Tortillas: 1 bánh',
         'Chop lettuce. Mix in a large bowl with the parmesan, dressing, and chopped bologna. Add filling to tortilla and roll up. Enjoy!'),
        ('69', 'Ham, Egg Beaters, and Mushroom Scramble', read_image('D:/synaptifit/streamlit/images/dishes/69.jpg'),
         '136;4;3;22',
         'Pam cooking spray: 0.6 g;Sliced ham: 2 oz;Mushrooms: 47 g;Egg: 120 g;Pepper: 0.1 g;Cayenne pepper: 0.36 g;Turmeric: 1/4 teaspoon',
         'Coat pan with non-stick spray and heat over medium. Chop mushrooms and ham. Sauté until mushrooms are tender;Whisk together the egg beaters with the pepper, cayenne, and turmeric. Pour over the mushrooms and ham and scramble until eggs have reached desired doneness. Serve immediately and enjoy!'),
        ('70', 'Salad with Ginger-Sesame-Miso Dressing', read_image('D:/synaptifit/streamlit/images/dishes/70.jpg'),
         '23;1;2;0',
         'Miso: 1 g;Rice wine vinegar: 1/2 teaspoon;Liquid aminos: 1/8 teaspoon;Sesame oil: 1/2 teaspoon;Ginger: 0.05 g;Water: 1/8 tablespoon;Lettuce: 12 g;Tomatoes: 5.6 g;Carrots: 4g',
         'Place miso, vinegar, liquid aminos, oil, ginger, and water into a blender or food processor. Blend until smooth;Combine chopped lettuce, tomatoes, and carrots. Add dressing and toss together.'),
        ('71', 'Sweet Potato Hash', read_image('D:/synaptifit/streamlit/images/dishes/71.jpg'), '304;32;15;11',
         'Red bell pepper: 60 g;Spinach: 60 g;Sweet potato: 130 g;Egg: 56 g;Avocado oil: 2 teaspoon',
         'Cook chopped bell pepper, spinach and shredded sweet potatoes in avocado oil for a few minutes, until spinach is just wilted and potatoes are tender, about 5 minutes;Cook egg in a non-stick frying pan until yolk has reached desired doneness. Serve on top of the potatoes/spinach mixture. Serve and enjoy!'),
        ('72', 'Cod Stir-Fry', read_image('D:/synaptifit/streamlit/images/dishes/72.jpg'), '303;15;7;45',
         'Cod: 230 g;Water: 240 g;Garlic: 3 g;Olive oil: 1 teaspoon;Cabbage: 140 g;Zucchini: 120 g;Fennel seed: 1 teaspoon;Curry powder: 1 teaspoon;Lemon juice: 6 g',
         'Heat a large pan or wok over medium-high heat. Add water and cod. Cover and let cook about 5 minutes. Add remaining ingredients and sauté for about 5 minutes. Serve immediately and enjoy!'),
        ('73', 'Parmesan and Mushroom Baked Eggs', read_image('D:/synaptifit/streamlit/images/dishes/73.jpg'),
         '244;4;18;16',
         'Olive oil: 1/2 tablespoon;Mushrooms: 72 g;Salt: 0.2 g;Pepper: 0.05 g;Egg: 2 fruit;Parmesan cheese: 2 teaspoon',
         'Preheat oven to 400 degrees F. Spray individual baking dishes for each serving or a flat casserole dish with non-stick spray;Wash mushrooms and spin dry or dry with paper towels. Slice mushrooms into slices about 1/2 inch thick;Heat oil in a large frying pan over high heat and sauté mushrooms until they have released all their liquid and the liquid has evaporated, about 6-8 minutes. Season mushrooms with a little salt and fresh ground black pepper and quickly transfer to baking dishes;Break half the eggs over the mushrooms in each individual dish (or all eggs over all the mushrooms in a casserole dish). Season eggs with a little salt and fresh ground black pepper to taste, and sprinkle with Parmesan cheese;Bake eggs until they are done to your liking, about 10 minutes for firm whites and partly-soft yolks. Serve hot, with toast if desired. Enjoy!'),
        ('74', 'Papaya Flaxseed Shake', read_image('D:/synaptifit/streamlit/images/dishes/74.jpg'), '124;16;5;6',
         'Water: 3 tablespoon;Flaxseed: 1 tablespoon;Papayas: 70 g;Plain yogurt: 6 tablespoon',
         'Combine all ingredients in a blender and pulse until smooth. Enjoy!'),
        ('75', 'Cottage Cheese Tuna Salad', read_image('D:/synaptifit/streamlit/images/dishes/75.jpg'), '322;9;5;61',
         'Pickles: 40 g;Jalapeno peppers: 1 fruit;Cottage cheese: 226 g;Tuna: 165 g;Mustard: 1 tablespoon',
         'Mince the pickles and jalapenos, and mix in with cottage cheese, tuna, and mustard. Mix together well and use as desired.'),
        (
        '76', 'Yogurt with Walnuts & Honey', read_image('D:/synaptifit/streamlit/images/dishes/76.jpg'), '260;16;10;28',
        'Walnuts: 15 g;Nonfat greek yogurt: 240 g;Honey: 1 teaspoon',
        'Rough-chop walnuts and mix into yogurt;Top with honey and enjoy!'),
        ('77', 'Cheat n Eat Vietnamese Chicken Soup', read_image('D:/synaptifit/streamlit/images/dishes/77.jpg'),
         '148;8;5;15',
         'Rice noodles: 7 g;Chicken breast: 2 oz;Peanut oil: 3/4 teaspoon;Garlic: 1.5 g;Ginger: 1/2 teaspoon;Crushed red pepper flakes: 0.02 g;Chicken broth: 240 g;Fish sauce: 1/2 tablespoon;Fresh cilantro: 1/2 tablespoon;Onions: 1/2 tablespoon;Basil: 1/4 tablespoon',
         'Soak noodles in very hot tap water. While noodles are soaking, cut chicken into thin julienne strips;Heat oil in deep skillet over medium-high heat, add chicken, garlic, ginger, and pepper flakes;Cook, stirring for 1 minute, then add broth and fish sauce and bring to a boil. Reduce heat to medium and simmer until chicken is done, about 8 minutes;Drain and arrange noodles in bottom of bowls, ladle soup over the top and sprinkle with cilantro, onion, and basil. Serve with sriracha or chili paste, if desired.'),
        ('78', 'Zucchini Hash', read_image('D:/synaptifit/streamlit/images/dishes/78.jpg'), '218;13;11;17',
         'Onions: 40 g;Zucchini: 124 g;Salt: 0.4 g;Pepper: 0.1 g;Pam cooking spray: 0.3 g;Egg: 2 fruit;Garlic powder: 1 teaspoon;Onion powder: 1 teaspoon',
         'Chop the onion and zucchini, and then mix everything up in a bowl;Heat a pan on medium heat, and lightly spray with a cooking spray;Spoon/pour the mixture into the pan. Cook about 5 minutes and flip. Cook another 5 min.'),
        ('79', 'Bean Sprouts with Tofu', read_image('D:/synaptifit/streamlit/images/dishes/79.jpg'), '140;7;9;9',
         'Mung beans: 52 g;Olive oil: 1/2 tablespoon;Tofu: 3 oz;Garlic: 1.5 g;Soy sauce: 1/2 tablespoon;Scallions: 12.5 g',
         'Rinse the sprouted mung beans with cold running water, drained and set aside. Remove the roots if you desire;Heat up a wok and add some cooking oil for pan-frying the tofu. When the oil is fully heated, pan-fry the tofu until they turn light brown on the surface. Transfer them to a dish lined with paper towels;Leave about 1 tablespoon of oil in the same wok, stir-fry the garlic until aromatic, then add the tofu back into the wok for a few quick stirs before adding the mung beans. Add soy sauce, scallions, and do a few more quick stirs. Plate and serve immediately.'),
        (
        '80', 'Avocado', read_image('D:/synaptifit/streamlit/images/dishes/80.jpg'), '322;17;29;4', 'Avocados: 1 fruit',
        'Cut in half and remove the pit;Optional topping ideas: Sea salt, black pepper, balsamic vinegar, lemon/lime juice, or paprika.'),
        ('81', 'Spinach and Mushroom Breakfast Scramble', read_image('D:/synaptifit/streamlit/images/dishes/81.jpg'),
         '192;6;5;30', 'Coconut oil: 1 teaspoon;Garlic: 3 g;Mushrooms: 70 g;Egg white: 243 g;Spinach: 30 g',
         'Add coconut oil, garlic, and mushrooms to pan over medium heat;Once mushrooms are slightly softened, add egg whites and mix well. When egg whites are almost cooked, add spinach and stir until spinach is wilted. Serve immediately and enjoy.'),
        (
            '82', 'Salami Cream Cheese Sandwich', read_image('D:/synaptifit/streamlit/images/dishes/82.jpg'),
            '553;32;36;25',
            'Cream cheese: 8 oz;Scallions: 6 g;Dill: 0.5 g;Garlic: 0.75 g;White bread: 2 slices;Lettuce: 28 g;Italian salami: 70 g',
            'In a small bowl, combine 8 oz cream cheese, ¼ cup green onions, ¼ cup dill, and press in 1 garlic clove. Mash herbs into the cream cheese;Spread about 1-2 tbsp of the cream cheese mixture on one side of each bread slice;Top with lettuce and about 6-8 pieces of salami, or to taste. Enjoy!'),
        ('83', 'Ham and Avocado Egg Wrap', read_image('D:/synaptifit/streamlit/images/dishes/83.jpg'), '231;6;18;12',
         'Butter: 1 teaspoon;Egg: 1 fruit;Avocados: 50 g;Sliced ham: 30 g',
         'Heat a small nonstick skillet over medium heat. Grease with butter or oil;In a bowl, crack one egg and mix well with a fork. Pour into a hot pan and tilt pan to spread egg into a large circle on the bottom of the pan into a tortilla shape;Let cook 30 seconds or until the bottom is set. Carefully flip with a large spatula and let cook another 30 seconds;Remove from pan. Let egg wrap cool slightly (or fully), top as desired with ham and avocado, roll and serve warm or cold.'),
        (
            '84', 'Toasted Pita with Gouda, Avocado, and Tomato',
            read_image('D:/synaptifit/streamlit/images/dishes/84.jpg'),
            '308;41;13;11', 'Pita bread: 1 bánh;Gouda cheese: 14 g;Tomatoes: 40 g;Avocados: 50 g',
            'Toast pita;Mash avocado and spread into pita pocket;Top with gouda and sliced tomato. Enjoy!'),
        ('85', 'Turkey Hummus Wrap', read_image('D:/synaptifit/streamlit/images/dishes/85.jpg'), '429;31;20;34',
         'Tortillas: 1 bánh;Sliced turkey: 116 g;Lettuce: 24 g;Avocados: 68 g;Tomatoes: 62 g;American cheese: 42 g;Hummus: 2 tablespoon',
         'Slather hummus onto tortilla;Layer with turkey, lettuce, avocado, tomato, and cheese;Roll up and enjoy!'),
        ('86', 'Meditteranean Salad', read_image('D:/synaptifit/streamlit/images/dishes/86.jpg'), '103;17;2;6',
         'Lettuce: 28 g;Cucumber: 75 g;Kidney beans: 64 g;Hummus: 1 tablespoon;Red wine vinegar: 1 tablespoon;Oregano: 1 tablespoon',
         'Chop lettuce and cucumber. Drain kidney beans. Whisk together hummus, red wine vinegar, and oregano. Toss all ingredients together in a bowl and enjoy!'),
        ('87', 'Black Bean and Bacon Soup', read_image('D:/synaptifit/streamlit/images/dishes/87.jpg'), '148;24;2;8',
         'Canned black beans: 130 g;Onions: 3 g;Vegetable Broth: 90 g;Salsa verde: 1 tablespoon;Cumin: 1/4 tablespoon;Bacon: 3 g',
         'Drain and rinse the beans. Thinly slice the green onion;In an electric food processor or blender, combine beans, broth, salsa, and cumin. Blend until fairly smooth;Heat the bean mixture in a saucepan over medium heat until thoroughly heated;Cook bacon in a pan over medium-high heat until bacon has reached desired crispiness. Chop and mix into the bean soup. Enjoy!'),
        ('88', 'Basic Vegetable Juice', read_image('D:/synaptifit/streamlit/images/dishes/88.jpg'), '390;92;2;12',
         'Carrots: 512 g;Red cabbage: 90 g;Spinach: 170 g;Pineapple: 226 g',
         'Juice carrots and cabbage;Blend juice with spinach and pineapple.'),
        ('89', 'Brie cheese on bread', read_image('D:/synaptifit/streamlit/images/dishes/89.jpg'), '204;18;10;11',
         'Multi-grain bread: 1 slices;Brie cheese: 1 oz', 'Spread cheese on bread, eat.'),
        ('90', 'Post-Workout Banana Protein Smoothie', read_image('D:/synaptifit/streamlit/images/dishes/90.jpg'),
         '225;30;1;25', 'Water: 470 g;Banana: 1 fruit;Whey protein powder: 30 g',
         'Combine all ingredients in a blender and pulse until smooth. Enjoy!'),
        ('91', 'Hummus Chickpea Snack Sandwiches', read_image('D:/synaptifit/streamlit/images/dishes/91.jpg'),
         '142;21;4;7',
         'Chickpeas: 40 g;Hummus: 20 g;Celery: 3 g;Whole-wheat bread: 1 slices;Pickles: 6 g;Roasted Red Peppers: 4.5 g',
         'Place chickpeas in a large bowl and mash lightly with a fork. Add hummus and mix;Chop celery and stir into hummus mix;Slice pickle into thin rounds and line half the slices bread with these slices. Divide chickpea salad evenly over the slices. Top with roasted red pepper slices and remaining slices of bread. Press down lightly. If desired, cut away edges then cut each sandwich in half to make snack-sized sandwiches. Store in a covered container until ready to serve.'),
        (
            '92', 'Breakfast Sandwich with Egg, Cheese, and Ham',
            read_image('D:/synaptifit/streamlit/images/dishes/92.jpg'),
            '298;29;12;21', 'English muffins: 1 bánh;Egg: 1 fruit;Honey ham: 1 oz;Cheddar cheese: 14 g',
            'Toast English muffin. Spray and pan over medium heat with non stick spray. Whisk together eggs in a bowl and pour into pan. Cook to desired doneness and set aside;Top toasted english muffin with ham, egg, and cheese. Return to toaster for a few more minutes to melt cheese. Enjoy!'),
        ('93', 'Raspberry Coconut Smoothie', read_image('D:/synaptifit/streamlit/images/dishes/93.jpg'), '531;88;22;5',
         'Raspberries: 250 g;Banana: 1/2 fruit;Coconut milk: 80 g;Chia seeds: 1/2 tablespoon',
         'Blend all ingredients until smooth.'),
        ('94', 'Strawberry Pear Juice', read_image('D:/synaptifit/streamlit/images/dishes/94.jpg'), '129;34;1;1',
         'Pears: 1 fruit;Raspberries: 30 g;Strawberries: 36 g',
         'Core pear. Juice ingredients and mix together well just before serving. Enjoy!')

    ]

    cursor.executemany('''
    INSERT OR IGNORE INTO Dish (Id, Name, Image, Nutrition, Recipe, Steps) VALUES (?, ?, ?, ?, ?, ?)
    ''', dish_data)
    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("Database initialized and tables created successfully!")


# Call the init_db function to initialize the database
init_db()


# Function to insert user data into the user_data table
def insert_user_data(username, age, level, workout_plan):
    conn = sqlite3.connect('fitness.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO user_data (username, age, level, workout_plan)
            VALUES (?, ?, ?, ?)
        ''', (username, age, level, workout_plan))
        conn.commit()
        print(f"Inserted user data: Username={username}, Age={age}, Level={level}, Workout Plan={workout_plan}")
    except sqlite3.Error as e:
        print(f"Error inserting user data: {e}")
    finally:
        conn.close()


# Function to insert workout data into the workouts table
def insert_workout_data(username, name, description, level, duration):
    conn = sqlite3.connect('fitness.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO workouts (username, name, description, level, duration)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, name, description, level, duration))
        conn.commit()
        print(
            f"Inserted workout data: Username={username}, Name={name}, Description={description}, Level={level}, Duration={duration}")
    except sqlite3.Error as e:
        print(f"Error inserting workout data: {e}")
    finally:
        conn.close()


# Function to insert contact message into the contact_messages table
def insert_contact_message(name, email, message):
    print(f"Debug - Inserting Contact Message: {name}, {email}, {message}")  # Debug
    conn = sqlite3.connect('fitness.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO contact_messages (name, email, message)
            VALUES (?, ?, ?)
        ''', (name, email, message))
        conn.commit()
        print(f"Inserted contact message: Name={name}, Email={email}, Message={message}")
    except sqlite3.Error as e:
        print(f"Error inserting contact message: {e}")
    finally:
        conn.close()


# Function to fetch user data from the user_data table
def fetch_user_data(username):
    conn = sqlite3.connect('fitness.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_data WHERE username = ?', (username,))
    data = cursor.fetchall()
    conn.close()
    return data


def fetch_workouts(username):
    conn = sqlite3.connect('fitness.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM workouts WHERE username = ?', (username,))
    data = cursor.fetchall()
    conn.close()
    return data


# Function to display contact messages
def display_contact_messages():
    messages = get_all_contact_messages()
    for message in messages:
        st.write(f"Name: {message[1]}")
        st.write(f"Email: {message[2]}")
        st.write(f"Message: {message[3]}")
        st.write(f"Date: {message[4]}")
        st.write("---")


# Function to display diets
def display_diets():
    diets = get_all_diets()
    for diet in diets:
        st.write(f"Diet Name: {diet[1]}")
        st.write(f"Description: {diet[2]}")
        st.write(f"Type: {diet[3]}")
        st.write(f"Calories: {diet[4]}")
        st.write("---")


# Function to display medicines
def display_medicines():
    medicines = get_all_medicines()
    for medicine in medicines:
        st.write(f"Medicine Name: {medicine[1]}")
        st.write(f"Dosage: {medicine[2]}")
        st.write(f"Frequency: {medicine[3]}")
        st.write(f"Side Effects: {medicine[4]}")
        st.write("---")


# Function to display workouts
def display_workouts():
    workouts = fetch_workouts(st.session_state.username)
    for workout in workouts:
        st.write(f"Workout Name: {workout[2]}")
        st.write(f"Description: {workout[3]}")
        st.write(f"Level: {workout[4]}")
        st.write(f"Duration: {workout[5]} minutes")
        st.write("---")


# Page Basic info
st.set_page_config(
    page_title='Smart Fitness Tracker with Personalized Recommendations',
    page_icon='Fitness_bloom.png'
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "show_signup" not in st.session_state:
    st.session_state.show_signup = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Side bar initialization and creation
with st.sidebar:
    if st.session_state.logged_in:
        selected = option_menu(

            menu_title="SFTPR",
            options=[
                "Home", "Diet", "Workout Suggestion", "Medicine Recommender",
                "Progress Tracker", "Exercise Browser", "Rescipes Browser",
                "Health Tips", "Contact", "Settings"
            ],
            icons=[
                "house", "flower3", "wrench", "clipboard2-x",
                "bar-chart", "trophy", "people",
                "heart-pulse", "envelope", "gear"
            ],
            menu_icon="cast",
            default_index=0
        )
        if st.session_state.username:
            st.markdown(f"### Hello, **{st.session_state.username}** 👋")
        else:
            st.markdown("### Hello, Guest 👋 (Please login!)")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.success("Logged out successfully!")
            st.experimental_rerun()
    else:
        selected = "Login"


def register_user(username, password):
    """Register a new user."""
    conn = sqlite3.connect('fitness.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (username, password)
            VALUES (?, ?)
        ''', (username, password))
        conn.commit()
        st.success("Registration successful! Please log in.")
        st.session_state.show_signup = False  # Redirect to login after registration
    except sqlite3.IntegrityError:
        st.error("Username already exists. Please choose a different username.")
    except Exception as e:
        st.error(f"Error during registration: {e}")
    finally:
        conn.close()


def login_user(username, password):
    """Authenticate a user."""
    conn = sqlite3.connect('fitness.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id FROM users WHERE username = ? AND password = ?
    ''', (username, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        st.session_state.user_id = user[0]
        st.session_state.username = username  # Store username in session state
        st.session_state.logged_in = True
        st.success(f"🎉 Logged in as **{username}**")
        st.experimental_rerun()
    else:
        st.error("❌ Invalid username or password.")


# Login Page
def login_page():
    # Ensure session state variables do not persist unwanted values
    if "login_username" in st.session_state:
        del st.session_state["login_username"]

    st.markdown("<h2 style='text-align: center; color: #4CAF50;'>Login</h2>", unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("👤 Username", placeholder="Enter your username", key="username_input")
        password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")

        if st.form_submit_button("Login", use_container_width=True):
            user = login_user(username, password)
            if user:
                st.session_state.user_id = user[0]
                st.session_state.username = username
                st.session_state.logged_in = True
                st.success(f"🎉 Logged in as **{username}**")
                st.experimental_rerun()
            else:
                st.error("❌ Invalid username or password.")

    if st.button("Don't have an account? Sign Up"):
        st.session_state.show_signup = True
        st.experimental_rerun()


def signup_page():
    st.markdown("<h2 style='text-align: center; color: #FF5733;'>Sign Up</h2>", unsafe_allow_html=True)
    with st.form("register_form"):
        new_username = st.text_input("👤 Choose a Username", key="register_username")
        new_password = st.text_input("🔑 Password", type="password", key="register_password")
        confirm_password = st.text_input("🔄 Confirm Password", type="password", key="confirm_password")

        if st.form_submit_button("Register", use_container_width=True):
            if new_password == confirm_password:
                register_user(new_username, new_password)
            else:
                st.error("❌ Passwords do not match.")

    if st.button("Already have an account? Login"):
        st.session_state.show_signup = False
        st.experimental_rerun()


if not st.session_state.logged_in:
    if st.session_state.show_signup:
        signup_page()
    else:
        login_page()


# Homepage
def homepage():
    st.title("Smart Fitness Tracker with Personalized Recommendations")
    words = '''
        <p style="font-style:italic; font-family:cursive;">
    Smart Fitness Tracker and Personalized Recommendations is an intelligent system that provides customized suggestions  
    for diet, medicine, and workout plans based on user data.
    </p>
    <p style="font-style:italic; font-family:cursive;">
    This machine learning-powered app uses collaborative and content-based filtering to generate personalized recommendations.
    </p>
    <p style="font-style:italic; font-family:cursive;">
    This is a prototype of the actual system, and we plan to introduce various enhancements in the future.
    </p>
    '''

    tech_stack = '''
        <ul>
            <li style="font-style:italic; font-family:cursive;">Dataset: CSV, JSON Files</li>
            <li style="font-style:italic; font-family:cursive;">Others libraries: Pandas, Numpy, Sklearn, Streamlit, Json</li>
            <li style="font-style:italic; font-family:cursive;">Programming: Python, Notebook</li>
            <li style="font-style:italic; font-family:cursive;">Visualization tools: Matplotlib, Plotly</li>
        </ul>
    '''

    image = Image.open('first.jpg')

    left_column, right_column = st.columns(2)
    with left_column:
        st.markdown(words, unsafe_allow_html=True)
    with right_column:
        st.image(image, use_column_width=True)

    st.title('Dataset')
    st.subheader("User Data from Database:")

    # Fetch user data using the username from session state

    files = load_data()

    json_files = get_suggestion(files, 10)
    data_files = get_data(json_files)

    st.dataframe(data_files)

    st.title('Tech Stack')
    st.markdown(tech_stack, unsafe_allow_html=True)


if selected == 'Home':
    homepage()


# Defining CSS file
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# Loading CSS
local_css('style.css')


def progress_tracker():
    st.title("🏋️ Track Your Progress")
    st.write("Log your workouts and health journey.")

    # User input fields
    username = st.text_input("Enter Your Username")
    weight = st.number_input("Enter Your Current Weight (kg)", min_value=30.0, max_value=200.0)
    calories = st.number_input("Calories Burned Today", min_value=0)
    diet = st.text_area("Describe Your Diet")
    workout = st.text_area("Describe Your Workout")
    progress = st.text_area("Your Overall Progress Notes")

    if st.button("Save Progress"):
        if username:
            conn = sqlite3.connect('fitness.db')
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO progress_tracker (username, weight, calories_burned, diet, workout, progress)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (username, weight, calories, diet, workout, progress))
            conn.commit()
            conn.close()
            st.success("✅ Progress saved successfully!")
        else:
            st.warning("⚠️ Please enter a username.")

    # Fetch and visualize data
    st.subheader("📊 Your Progress Overview")
    conn = sqlite3.connect('fitness.db')
    df = pd.read_sql("SELECT * FROM progress_tracker WHERE username = ?", conn, params=(username,))
    conn.close()

    if not df.empty:
        st.write("### Recent Entries")
        st.dataframe(df)

        # Weight Progress Chart
        st.write("### 📉 Weight Progress Over Time")
        fig, ax = plt.subplots()
        ax.plot(df['timestamp'], df['weight'], marker='o', linestyle='-')
        ax.set_xlabel("Date")
        ax.set_ylabel("Weight (kg)")
        ax.set_title("Weight Progress")
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # Calories Burned Chart
        st.write("### 🔥 Calories Burned Over Time")
        fig, ax = plt.subplots()
        ax.bar(df['timestamp'], df['calories_burned'], color='orange')
        ax.set_xlabel("Date")
        ax.set_ylabel("Calories Burned")
        ax.set_title("Calories Burned Progress")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.info("ℹ️ No progress data found. Start logging your progress!")


if selected == "Progress Tracker":
    progress_tracker()

# Set initial theme to Dark
if "theme" not in st.session_state:
    st.session_state.theme = "dark"  # Default to dark mode


def apply_theme():
    """Applies the selected theme using CSS injection."""
    if st.session_state.theme == "dark":
        dark_theme = """
        <style>
            body, .stApp { background-color: #0E1117; color: #FFFFFF; }

            /* Text and headings */
            h1, h2, h3, h4, h5, h6, p, div, span, label { color: #FFFFFF; }


            /* Input fields */
            .stTextInput>div>div>input, .stTextArea>div>div>textarea { 
                color: #FFFFFF; 
                background-color: #1E1E1E; 
                border: 1px solid #333333;
            }

            /* Select boxes */
            .stSelectbox>div>div>select, .stRadio>div>div>label { 
                color: #FFFFFF; 
                background-color: #1E1E1E; 
            }

            /* Buttons */
            .stButton>button { 
                color: #FFFFFF; 
                background-color: #4CAF50; 
                border: 1px solid #4CAF50; 
            }

            /* Dataframes */
            .stDataFrame { color: #FFFFFF; background-color: #1E1E1E; }
        </style>
        """
        st.markdown(dark_theme, unsafe_allow_html=True)

    else:
        light_theme = """
    <style>
    body, .stApp { background-color: #FFFFFF; color: #000000; }

    /* Text and headings */
    h1, h2, h3, h4, h5, h6, p, div, span, label { color: #000000 !important; }

    /* Input fields */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { 
        color: #000000 !important; 
        background-color: #F0F2F6 !important; 
        border: 1px solid #CCCCCC !important;
    }

    /* Select boxes & Radio buttons */
    .stSelectbox>div>div>select, .stRadio>div>div>label { 
        color: #FFFFFF !important; 
        background-color: #F0F2F6 !important; 
    }

    /* Fix for dropdown options */
    .stSelectbox>div>div>select option {
        color: #FFFFFF !important;
        background-color: #FFFFFF !important;
    }

    /* Buttons */
    .stButton>button { 
        color: #FFFFFF !important; 
        background-color: #4CAF50 !important; 
        border: 1px solid #4CAF50 !important; 
    }

    /* Dataframes */
    .stDataFrame { color: #000000 !important; background-color: #F0F2F6 !important; }
   </style>

        """
        st.markdown(light_theme, unsafe_allow_html=True)


def settings():
    st.title("Settings")

    # Theme Selection Dropdown
    theme = st.selectbox("Choose Theme", ["Dark", "Light"], index=0 if st.session_state.theme == "dark" else 1)

    # Update theme state
    st.session_state.theme = "light" if theme == "Light" else "dark"

    # Apply selected theme
    apply_theme()
    st.success(f"Theme set to {theme} mode!")


# Apply theme at startup
apply_theme()

if selected == "Settings":
    settings()

# Custom CSS for Improved Styling
st.markdown("""
    <style>
        .tip-box {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 2px 4px 10px rgba(0, 0, 0, 0.1);
            font-size: 20px;
            text-align: center;
            color: #333;
            font-weight: bold;
            margin: 20px auto;
            width: 80%;
        }

        .btn-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 15px;
        }

        .btn {
            background: linear-gradient(135deg, #4CAF50, #45a049);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s ease, box-shadow 0.3s ease;
        }

        .btn:hover {
            transform: scale(1.05);
            box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2);
        }

        .btn-wrapper {
            display: flex;
            justify-content: center;
            margin-top: 15px;
        }
    </style>
""", unsafe_allow_html=True)


def health_tips():
    st.title("💡 Daily Health Tips")

    tips = [
        "💧 **Stay Hydrated:** Drink at least 2 liters of water daily.",
        "🏋️ **Stay Active:** Exercise at least 30 minutes every day.",
        "🥦 **Eat Right:** Include fiber, protein, and healthy fats in your diet.",
        "😴 **Get Enough Sleep:** Aim for 7-9 hours of sleep for better health.",
        "👀 **Reduce Screen Time:** Take short breaks to rest your eyes.",
        "🧘 **Practice Mindfulness:** Deep breathing helps reduce stress.",
        "🪑 **Improve Posture:** Sit upright to avoid back pain.",
        "🚫🍭 **Limit Sugar Intake:** Too much sugar can lead to health issues."
    ]

    if "tip_index" not in st.session_state:
        st.session_state.tip_index = 0

    # Display current tip inside a styled box
    st.markdown(
        f'<div style="background-color: {"#1E1E1E" if st.session_state.theme == "dark" else "#F0F2F6"}; '
        f'padding: 20px; border-radius: 10px; color: {"#FFFFFF" if st.session_state.theme == "dark" else "#000000"};'
        f'">{tips[st.session_state.tip_index]}</div>',
        unsafe_allow_html=True
    )

    # Centered navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        btn_prev, btn_next = st.columns([1, 1])

        with btn_prev:
            if st.button("⬅ Previous", key="prev_btn"):
                st.session_state.tip_index = (st.session_state.tip_index - 1) % len(tips)

        with btn_next:
            if st.button("Next ➡", key="next_btn"):
                st.session_state.tip_index = (st.session_state.tip_index + 1) % len(tips)


if selected == "Health Tips":
    health_tips()


# Contact Form Frontend
def form():
    with st.container():
        st.write("---")
        st.header('Get In Touch With Me!')
        st.write('##')

        # Input fields for the contact form
        name = st.text_input('Your Full Name', key='name')
        email = st.text_input('Your Email ID', key='email')
        message = st.text_area('Your Message', key='message')

        # Submit button
        if st.button('Send'):
            # Check if all fields are filled
            if name and email and message:
                # Insert the contact message into the database
                insert_contact_message(name, email, message)
                st.success("Message sent successfully!")
            else:
                st.warning("Please fill in all fields before submitting.")


if selected == 'Contact':
    form()

# Exercise JSON Dataset
exercise_by_level = {
    'beginner': {
        'Monday': ['20 Squats', '10 Push-ups', '10 Lunges Each leg', '15 seconds Plank', '30 Jumping Jacks'],
        'Tuesday': ['20 Squats', '10 Push-ups', '10 Lunges Each leg', '15 seconds Plank', '30 Jumping Jacks'],
        'Wednesday': ['15 minutes Walk', '30 seconds Jump rope(2 reps)', '20 seconds Cobra Stretch'],
        'Thursday': ['25 Squats', '12 Push-ups', '12 Lunges Each leg', '15 seconds Plank', '30 Jumping Jacks'],
        'Friday': ['25 Squats', '12 Push-ups', '12 Lunges Each leg', '15 seconds Plank', '30 Jumping Jacks'],
        'Saturday': ['15 minutes Walk', '30 seconds Jump rope(2 reps)', '20 seconds Cobra Stretch']
    },
    'intermediate': {
        'Monday': ['3 Set Squats(8-12 reps)', '3 Set Leg Extension(8-12 reps)', '3 Set Lunges(10 reps Each)',
                   '30 Seconds Skipping(2 reps)'],
        'Tuesday': ['3 Set Bench Press(12 reps)', '3 Set Dumb-bell incline press(8-12 reps)',
                    '3 Set Cable Crossovers(10-12 reps)', '30 Seconds Boxing Skip(2 reps)'],
        'Wednesday': ['3 Set Deadlifts(6-12 reps)', '3 Set Barbell Curls(8-12 reps)', '3 Set Incline Curls(8-12 reps)'],
        'Thursday': ['3 Set Shoulder Press(8-10 reps)', '3 Set Incline Lateral Raises(8-10 reps)',
                     '3 Set Sit-ups(10-12 reps)', '2 Set Leg Raises(8-12 reps)'],
        'Friday': ['10 minutes Brisk Walk', '1 minute Skipping', 'Breathing Exercises'],
        'Saturday': ['10 minutes Brisk Walk', '1 minute Skipping', 'Breathing Exercises']
    },
    'advanced': {
        'Monday': ['5 Set Squats(8-12 reps)', '5 Set Leg Extension(8-12 reps)', '5 Set Lunges(10 reps Each)',
                   '60 Seconds Skipping(2 reps)'],
        'Tuesday': ['5 Set Bench Press(12 reps)', '5 Set Dumb-bell incline press(8-12 reps)',
                    '5 Set Cable Crossovers(10-12 reps)', '60 Seconds Boxing Skip(2 reps)'],
        'Wednesday': ['5 Set Deadlifts(6-12 reps)', '5 Set Barbell Curls(8-12 reps)', '5 Set Incline Curls(8-12 reps)'],
        'Thursday': ['5 Set Shoulder Press(8-10 reps)', '5 Set Incline Lateral Raises(8-10 reps)',
                     '5 Set Sit-ups(10-12 reps)', '4 Set Leg Raises(8-12 reps)'],
        'Friday': ['20 minutes Brisk Walk', '2 minute Boxing Skip', 'Breathing Exercises'],
        'Saturday': ['25 minutes Brisk Walk', '1 minute Skipping', 'Breathing Exercises']
    }
}


def generate_workout(level):
    # Return the workout plan for the selected level
    return exercise_by_level[level]


# For Workout Suggestion
if selected == 'Workout Suggestion':
    st.title('Personalized Workout Recommender')

    age = st.selectbox('Age', ['Select', 'Less than 18', '18 to 49', '49 to 60', 'Above 60'])
    duration = st.radio('Workout Duration:', ['Less frequently', 'Moderate', 'More Frequently'])
    level = st.selectbox('Select your level:', ['Select', 'beginner', 'intermediate', 'advanced'])
    button = st.button('Recommend Workout')

    if button:
        if level == 'Select':
            st.warning('Insertion error!! Re-check the input fields')
        else:
            nums = 1  # Initialize counter for days
            workout_plan = generate_workout(level)

            # Define days of the week explicitly
            days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            workout_data = []  # List to store workout details for visualization

            for day in days_of_week:
                if day == "Sunday":
                    st.markdown(
                        f"""
                        <h4>Your Workout Plan for Day {nums}: {day}</h4>
                        <div class="sundays">
                            <p style="color:#7FFF00; font-style:italic; font-family:cursive;">Take rest and go for a light walk in the park.</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    workout_data.append({"Day": day, "Workout Count": 0})  # No workouts on Sunday
                else:
                    exercises = exercise_by_level[level].get(day, ["No workout assigned"])
                    exercise_str = ", ".join(exercises)
                    insert_workout_data(st.session_state.username, f"Day {nums} Workout ({day})", exercise_str, level,
                                        30)

                    st.markdown(
                        f"""
                        <h4>Your Workout Plan for Day {nums}: {day}</h4>
                        <div class="workout">
                            <div class="workout-info">
                                <p style="color:#7FFF00; font-style:italic; font-family:cursive;">Workout: {exercise_str}</p>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    workout_data.append({"Day": day, "Workout Count": len(exercises)})

                nums += 1  # Increment day counter

            # Insert user workout details into the user_data table
            insert_user_data(st.session_state.username, age, level, str(workout_plan))

            # Convert data to Pandas DataFrame
            df = pd.DataFrame(workout_data)

            # Create a bar chart for workout distribution
            st.subheader("📊 Workout Distribution Over the Week")
            fig = px.bar(df, x="Day", y="Workout Count", title="Number of Workouts per Day",
                         labels={"Workout Count": "Number of Exercises"},
                         color="Workout Count", height=400)
            st.plotly_chart(fig)

# For Medicine Recommender
if selected == 'Medicine Recommender':
    main_1()

# For custom food recommendations
if selected == 'Diet':
    diet()


# Function to load exercises from SQLite
def load_exercises():
    conn = sqlite3.connect("fitness.db")  # Ensure correct database
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Exercise")
    exercises = cursor.fetchall()
    conn.close()
    return exercises


# Function to display the Exercise Browser
def exercise_browser():
    st.markdown("<h1 style='text-align: center'>Exercise Browser</h1>", unsafe_allow_html=True)

    exercises = load_exercises()
    exercise_keywords = [""] + [e[1] for e in exercises]  # e[1] is Exercise Name

    exercise_keyword = st.selectbox("**Search Exercise**", tuple(exercise_keywords))

    if exercise_keyword:
        conn = sqlite3.connect("fitness.db")  # Ensure correct database
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Exercise WHERE Name = ?", (exercise_keyword,))
        exercise_result = cursor.fetchone()
        conn.close()

        if exercise_result:
            st.markdown(f"<h2 style='text-align: center'>{exercise_result[1]}</h2>", unsafe_allow_html=True)

            col1, col2, col3 = st.columns([0.15, 1.7, 0.15])
            with col2:
                st.markdown(f"""
                    <iframe width="100%" height="500px" allow="fullscreen;" src="{exercise_result[2]}"></iframe>
                """, unsafe_allow_html=True)

                st.subheader("I. Overview")
                st.write(exercise_result[3].replace(';', '\n'))

                st.subheader("II. Instructions")
                instructions_list = exercise_result[4].split(';')
                instructions_html = "<ul style='list-style-type: decimal; padding-left: 22px'>"
                for instruction in instructions_list:
                    instructions_html += f"<li>{instruction}</li>"
                instructions_html += "</ul>"

                st.markdown(instructions_html, unsafe_allow_html=True)


if selected == "Exercise Browser":
    exercise_browser()


class Diet():
    def __init__(self, calories, nutrition, breakfast, lunch, dinner):
        self.calories = calories
        self.nutrition = nutrition
        self.breakfast = breakfast
        self.lunch = lunch
        self.dinner = dinner

    def get_nutrition_detail(self):
        tmp = self.nutrition.split(';')
        return NutritionDetail(float(tmp[0]), float(tmp[1]), float(tmp[2]), float(tmp[3]))

    def get_breakfast_detail(self):
        tmp = self.breakfast.split(':')
        calories = tmp[0]
        temp = tmp[1].split(';')
        id1, amount1 = temp[0].split('x')
        id2, amount2 = temp[1].split('x')
        return DietDetail(calories, id1, amount1, id2, amount2)

    def get_lunch_detail(self):
        tmp = self.lunch.split(':')
        calories = tmp[0]
        temp = tmp[1].split(';')
        id1, amount1 = temp[0].split('x')
        id2, amount2 = temp[1].split('x')
        return DietDetail(calories, id1, amount1, id2, amount2)

    def get_dinner_detail(self):
        tmp = self.dinner.split(':')
        calories = tmp[0]
        temp = tmp[1].split(';')
        id1, amount1 = temp[0].split('x')
        id2, amount2 = temp[1].split('x')
        return DietDetail(calories, id1, amount1, id2, amount2)


class NutritionDetail():
    def __init__(self, calories, carbs, fat, protein):
        self.calories = calories
        self.carbs = carbs
        self.fat = fat
        self.protein = protein

    def get_carbs_percentage(self):
        c = self.carbs * 4 / (self.carbs * 4 + self.fat * 9 + self.protein * 4)
        return c

    def get_fat_percentage(self):
        f = self.fat * 9 / (self.carbs * 4 + self.fat * 9 + self.protein * 4)
        return f

    def get_protein_percentage(self):
        p = self.protein * 4 / (self.carbs * 4 + self.fat * 9 + self.protein * 4)
        return p


class DietDetail():
    def __init__(self, calories, id1, amount1, id2, amount2):
        self.calories = calories
        self.id1 = id1
        self.amount1 = amount1
        self.id2 = id2
        self.amount2 = amount2


class Dish():
    def __init__(self, id, name, image, nutrition, recipe, steps):
        self.id = id
        self.name = name
        self.image = image
        self.nutrition = nutrition
        self.recipe = recipe
        self.steps = steps

    def get_nutrition_detail(self):
        tmp = self.nutrition.split(';')
        return NutritionDetail(float(tmp[0]), float(tmp[1]), float(tmp[2]), float(tmp[3]))

    def get_recipe_detail(self):
        tmp = self.recipe.split(';')
        ingredients = {}
        for s in tmp:
            temp = s.split(':')
            ingredients[temp[0]] = temp[1].strip()
        return RecipeDetail(ingredients)

    def get_steps_detail(self):
        tmp = self.steps.split(';')
        steps = {}
        for i in range(0, len(tmp)):
            key = 'Step ' + str(i + 1) + ':'
            value = tmp[i]
            steps[key] = value
        return StepsDetail(steps)


class RecipeDetail():
    def __init__(self, ingredients):
        self.ingredients = ingredients


class StepsDetail():
    def __init__(self, steps):
        self.steps = steps


# Function to load dishes from SQLite
def load_dishes():
    conn = sqlite3.connect("fitness.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Dish")
    dishes = cursor.fetchall()
    conn.close()
    return dishes


# Function to get dish details
def get_dish_by_name(name):
    conn = sqlite3.connect("fitness.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Dish WHERE Name = ?", (name,))
    dish = cursor.fetchone()
    conn.close()
    return dish


# Function to Display the Food & Recipe Browser
def food_browser():
    # Apply custom CSS styles inside the function
    st.markdown(
        f"""
            <style>
                .css-18ni7ap.e8zbici2 {{
                    opacity: 0;
                }}
                .css-h5rgaw.egzxvld1 {{
                    opacity: 0;
                }}
                .block-container.css-91z34k.egzxvld4 {{
                    width: 100%;
                    padding: 0.5rem 1rem 10rem;
                    max-width: none;
                }}
                .css-uc76bn.e1fqkh3o9 {{
                    padding-top: 2rem;
                    padding-bottom: 0.25rem;
                }}
            </style>
        """, unsafe_allow_html=True
    )

    # Center Logo and Title inside food_browser
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([0.5, 0.5, 1, 0.75, 1, 0.75, 0.5, 0.5])
    with col4:
        st.image(image='images/logo.png', width=140)

    # Main content of Food Browser starts here
    st.markdown("<h1 style='text-align: center'> Recipe Browser </h1>", unsafe_allow_html=True)

    dishes = load_dishes()
    dish_keywords = [""] + sorted([d[1] for d in dishes])  # d[1] is Dish Name

    dish_keyword = st.selectbox("**Search Dish**", tuple(dish_keywords))

    if dish_keyword:
        dish_result = get_dish_by_name(dish_keyword)

        if dish_result:
            dish_id, dish_name, dish_image, nutrition, recipe, steps = dish_result

            st.markdown(f"<h2 style='text-align: center'>{dish_name}</h2>", unsafe_allow_html=True)

            # Display Image (Handle NULL Values)
            col1, col2, col3 = st.columns([1.3, 0.55, 0.15])
            with col1:
                if dish_image:
                    encoded_image = base64.b64encode(dish_image).decode("utf-8")
                    st.markdown(
                        f"""
                            <p style="text-align: right">
                                <img src="data:image/jpeg;base64,{encoded_image}" width="90%">
                            </p>
                            """, unsafe_allow_html=True
                    )
                else:
                    st.warning("⚠ No image available for this dish.")

            # Display Nutrition Info
            with col2:
                nutrition_values = nutrition.split(";") if nutrition else ["0", "0", "0", "0"]
                cal, carbs, fat, protein = map(float, nutrition_values)  # Convert to float

                st.markdown(f"""
                        <table style="width:100%">
                            <tr><th style="font-size: 22px;">Nutrition</th></tr>
                            <tr>
                                <td>
                                    <b>Calories:</b> <text style="float:right">{round(cal)} cal</text><br/>
                                    <b>Carbs:</b> <text style="float:right">{carbs} g</text><br/>
                                    <b>Fat:</b> <text style="float:right">{fat} g</text><br/>
                                    <b>Protein:</b> <text style="float:right">{protein} g</text><br/>
                                </td>
                            </tr>
                        </table>
                        <br/>
                        <div class="figure_title" style="text-align:center; font-size:20px"><b>Percent Calories From:</b></div>
                    """, unsafe_allow_html=True)

                # Pie Chart for Nutrition Distribution
                matplotlib.rcParams.update({'font.size': 5})
                labels = ['Carbs', 'Fat', 'Protein']
                colors = ['#F7D300', '#38BC56', '#D35454']
                data = [carbs, fat, protein]
                fig, ax = plt.subplots(figsize=(1, 1))
                ax.pie(data, labels=labels, colors=colors, explode=(0.15, 0.075, 0.075), autopct='%1.1f%%',
                       startangle=90,
                       wedgeprops={"edgecolor": "black", 'linewidth': 1, 'antialiased': True})
                ax.axis('equal')
                st.pyplot(fig)

            # Display Recipe & Steps
            col1, col2, col3, col4 = st.columns([0.122, 0.45, 1.278, 0.15])

            # Recipe Section
            with col2:
                recipe_table = "<table style='width: 100%;'><tr><th style='font-size: 22px;'>Recipe</th></tr><tr><td>"
                if recipe:
                    for item in recipe.split(";"):
                        ingredient, amount = item.split(":")
                        recipe_table += f"<b>{ingredient}:</b> <text style='float:right'>{amount}</text><br/>"
                else:
                    recipe_table += "No recipe available."
                recipe_table += "</td></tr></table>"
                st.markdown(recipe_table, unsafe_allow_html=True)

            # Steps Section
            with col3:
                steps_table = "<table style='width: 100%;'><tr><th colspan='2' style='font-size: 22px;'>Steps to Cook</th></tr>"
                if steps:
                    for i, step in enumerate(steps.split(";"), 1):
                        steps_table += f"<tr><td style='width: 80px; vertical-align: top'><b>Step {i}</b></td><td>{step}</td></tr>"
                else:
                    steps_table += "<tr><td>No steps available.</td></tr>"
                steps_table += "</table>"
                st.markdown(steps_table, unsafe_allow_html=True)


if selected == "Rescipes Browser":
    food_browser()

