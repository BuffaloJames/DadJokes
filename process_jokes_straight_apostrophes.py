# Python script to process the provided joke list and create jokes.json
# with straight apostrophes.

import json
import re

JOKE_DATA = """
I’m afraid for the calendar. Its days are numbered.
Why do fathers take an extra pair of socks when they go golfing?In case they get a hole in one!
Singing in the shower is fun until you get soap in your mouth. Then it’s a soap opera.
What do a tick and the Eiffel Tower have in common?They’re both Paris sites.
What do you call a fish wearing a bowtie? Sofishticated.
If April showers bring May flowers, what do May flowers bring? Pilgrims.
What do you call a factory that makes okay products? A satisfactory.
Have you heard about the chocolate record player? It sounds pretty sweet.
I only know 25 letters of the alphabet. I don’t know y.
What did one wall say to the other? I’ll meet you at the corner.
Where do fruits go on vacation?Pear-is!
What’s the best thing about Switzerland? I don’t know, but the flag is a big plus.
What does a sprinter eat before a race? Nothing, they fast!
What has more letters than the alphabet? The post office!
What do you call a poor Santa Claus? St. Nickel-less. %%Christmas
How do you get a squirrel to like you? Act like a nut.
Why don’t eggs tell jokes? They’d crack each other up. %%Food
I don’t trust stairs. They’re always up to something.
What do you call someone with no body and no nose? Nobody knows.
Did you hear the rumor about butter? Well, I’m not going to spread it! %Food
Why couldn’t the bicycle stand up by itself? It was two tired.
What did one hat say to the other? Stay here! I’m going on ahead.
This graveyard looks overcrowded. People must be dying to get in.
What does a lemon say when it answers the phone? Yellow! %%Food
Why can’t a nose be 12 inches long? Because then it would be a foot.
What kind of car does an egg drive? A yolkswagen. %%Food
How do you make 7 even? Take away the s.
How many tickles does it take to make an octopus laugh? Ten tickles.
Why don’t eggs tell jokes? They’d crack each other up. %Food
What do you call an angry carrot? A steamed veggie. %%Food
It takes guts to be an organ donor.
How do you make a tissue dance? You put a little boogie in it.
Why did the math book look so sad? Because of all of its problems! %%School
What do you call cheese that isn’t yours? Nacho cheese. %%Food
How does a penguin build its house? Igloos it together.
What country’s capital is growing the fastest? Ireland. Every day it’s Dublin.
I’m on a seafood diet. I see food and I eat it. %%Food
Why did the scarecrow win an award? Because he was outstanding in his field.
I made a pencil with two erasers. It was pointless.
I’m reading a book about anti-gravity. It’s impossible to put down!
Did you hear about the guy who invented the knock-knock joke? He won the ’no-bell’ prize.
I’ve got a great joke about construction, but I’m still working on it.
I used to hate facial hair...but then it grew on me.
I decided to sell my vacuum cleaner—it was just gathering dust!
You know, people say they pick their nose, but I feel like I was just born with mine.
What’s brown and sticky? A stick.
What do you call an elephant that doesn’t matter? An irrelephant. %%Animal
What do you get from a pampered cow? Spoiled milk.
If you see a crime at an Apple Store, does that make you an iWitness?
I was going to tell a time-traveling joke, but you guys didn’t like it.
What do you call a fake noodle? An impasta. %%Food
What do you call a belt made of watches? A waist of time.
What do you call a pony with a sore throat? A little hoarse. %%Animal
Mountains aren’t just funny. They’re hill areas.
How much does it cost Santa to park his sleigh? Nothing, it’s on the house. %%Christmas
What’s a robot’s favorite snack? Computer chips. %%Food
Why are piggy banks so wise? They’re filled with common cents.
How do you get a good price on a sled? You have toboggan. %%Winter
Where do young trees go to learn? Elementree school %%School
Wanna hear a joke about paper? Never mind—it’s tearable.
I could tell a joke about pizza, but it’s a little cheesy. %%Food
Don’t trust atoms. They make up everything!
When does a joke become a dad joke? When it becomes apparent.
I don’t play soccer because I enjoy the sport. I’m just doing it for kicks! %%Sports
Which state has the most streets? Rhode Island.
Did you hear about the fire at the shoe factory? Unfortunately, many soles were lost.
What do you call a pig who knows how to use a knife? A pork chop. %%Food
Why did the pony ask for a glass of water? Because it was a little horse. %%Animal
How many apples can you grow on a tree? All of them. %%Food
What do kids play when they have nothing else to do? Bored games.
What kind of music do elves listen to? Wrap music. %%Christmas
What does cake and baseball have in common? They both need a batter. %%Sports
When does Friday come before Thursday? In the dictionary.
How can you tell if a pig is hot? It’s bacon. %%Food
What do you call a rude cow? Beef jerky %%Animal
How do you get a squirrel’s attention? Act like a nut. %%Animal
Did you hear about the cat that ate a lemon? Now it’s a sour puss. %%Animal
What did one volcano say to the other? I lava you.
How do mice floss their teeth? With string cheese. %%Animal
How do you cook an alligator? With a croc-pot. %%Animal
What did the earthquake say when it was done? Sorry, my fault!
Why did the computer go to bed? It needed to crash.
What kind of bug can tell time? A clock-roach. %%Animal
What do you call a can opener that doesn’t work? A can’t opener.
What do pigs use to clean up? Hogwash. %%Animal
What’s a pirate’s favorite letter? You’d think it’s the R, but it’s really the C. %%Pirate
When is a door not a door? When it’s ajar.
Did you hear about the broken guitar for sale? It comes with no strings attached.
Once I read a book about glue. I couldn’t put it down.
What do you call a fish with no eyes? Fsh. %%Animal
What should you do if you meet a giant? Use big words.
What do you call a cow with two legs? Lean beef. %%Animal
What sits on the seabed and has anxiety? A nervous wreck.
What’s the best air to breathe if you want to be rich? Millionaire.
Why did the girl toss a clock out the window? She wanted to see time fly.
Where do armies belong? In your sleeves.
Where did the king put his armies? In his sleevies!
What did one plate say to another plate? Tonight, dinner’s on me.
What happens when doctors get frustrated? They lose their patients.
What do you call a bear with no teeth? A gummy bear. %%Animal
What invention allows us to see through walls? Windows.
What’s orange and sounds like a parrot? A carrot. %%Animal
Why did the coach go to the bank? To get his quarter back. %%Sports
Why do nurses like red crayons? Sometimes they have to draw blood.
What kind of jewelry do rabbits wear? 14 carrot gold. %%Animal
Why can’t the pirate learn the alphabet? Because he kept getting lost at C. %%Pirate
What do you call a cheese that isn’t yours? Nacho cheese! %%Food
How do celebrities keep cool? They have many fans.
What did the janitor say when he jumped out of the closet? Supplies!
What’s more unbelievable than a talking dog? A spelling bee. %%Animal
What do you call a cow with no legs? Ground beef. %%Animal
What do you call a happy cowboy? A jolly rancher.
Why shouldn’t you trust trees? They seem shady.
How do you fix a broken tomato? With tomato paste. %%Animal
What kind of music scares balloons? Pop music.
Why did the orange stop halfway across the road? It ran out of juice. %%Animal %%Cross the road
Why did the Oreo go to the dentist? It lost its filling. %%Animal
How do you get an astronaut’s baby to stop crying? You rocket.
What do dogs and phones have in common? Both have collar ID. %%Animal
Why shouldn’t you play poker in the jungle? Too many cheetahs. %%Animal
What sounds like a sneeze and is made of leather? A shoe.
How do you stop a bull from charging? You cancel its credit card. %%Animal
Why was the math book sad? It had too many problems. %%School
Why are fish so smart? Because they swim in schools. %%School
Why did the employee get fired from the keyboard factory? He wasn’t putting in enough shifts.
Did you hear about the man who cut off his left leg? He’s all right now.
Did you hear the one about the claustrophobic astronaut? He just needed a little space.
What kind of music should you listen to while fishing? Something catchy!
What do you call a girl in the middle of a tennis court? Annette. %%Sports
What did the ocean say to the beach? Nothing. It just waved. %%Beach
What did one wall say to the other? I’ll meet you at the corner.
Why did the nose feel sad? It was always getting picked on.
Did you hear about the cold dinner? It was chili. %%Food
Why did the deer go to the dentist? It had buck teeth. %%Animal
Why can’t you trust a balloon? It’s full of hot air.
A cheese factory exploded in France. Da brie is everywhere! %%Animal
Not sure if you have noticed, but I love bad puns. That’s just how eye roll.
Why did the banana go to the doctor? Because it wasn’t peeling well. %%Food
Where does a sheep go to get a haircut? The baa baa shop. %%Animal
What did the mama cow say to the baby cow? It’s pasture bed time. %%Animal
Why should you never use a dull pencil? Because it’s pointless.
Why did the cookie go to the doctor? It was feeling crumby. %%Food
Where did the cat go after losing its tail? The retail store. %%Animal
Why don’t eggs tell jokes? They’d crack each other up. %%Food
What kind of sandals do frogs wear? Open-toad. %%Animal
What do you call a herd of sheep falling down a hill? A lambslide. %%Animal
How do you organize a space party? You planet.
How many tickles does it take to make an octopus laugh? Ten tickles. %%Animal
What do you call a potato wearing glasses? A spec-tater. %%Food
What do you call a moose with no name? Anonymoose. %%Food
Why did the ram run over the cliff? He didn’t see the ewe turn. %%Animal
Why did the picture go to jail? He was framed.
What is a calendar’s favorite food? Dates.
Why was the football stadium cold? There were too many fans. %Sports
Why do bananas wear sunscreen? Because they peel. %%Food
Why do bees have sticky hair? Because they use honey combs. %Animal
Why did the watch go on vacation? To unwind.
How does a penguin build a house? Igloos it together. %%Animal
Why do melons have weddings? Because they cantaloupe.
Why did the computer get glasses? To improve its website.
What did the blanket say to the bed? I’ve got you covered.
What did the roof say to the shingle? The first one’s on the house.
What do you call birds that stick together? Velcrows %%Animal
Why did the duck fall on the sidewalk? He tripped on a quack. %%Animal
How do birds learn to fly? They wing it. %%Animal
Did you hear about the walnut and cashew that threw a party? It was nuts. %%Food
Did the hear about the ice cream truck accident? It crashed on a rocky road.
What kind of bird works on a construction site? A crane. %%Animal
What did one elevator say to the other elevator? I think I’m coming down with something.
What did the hamburger name its baby? Patty.
What type of music do the planets enjoy? Neptunes.
Why did the phone wear glasses? Because it lost all its contacts.
Why do bakers work so hard? Because they knead dough.
Why are fish so easy to weigh? Because they have their own set of scales.
What do you call a priest that becomes a lawyer? A father-in-law.
What do you give a scientist with bad breath? Experi-mints.
What did Benjamin Franklin say when he discovered electricity? Nothing. He was too shocked.
What do you call a medieval lamp? A knight light.
What did one hat say to the other? You go on ahead.
Why did the frog take the bus to work? His car got toad.
What does an evil hen lay? Deviled eggs.
How can you tell the difference between a dog and tree? By their bark.
Why do dragons sleep during the day? Because they like to fight knights.
Why did the scarecrow win an award? It was outstanding in his field.
Did you hear about the 12-inch dog? It was a foot long.
Why did the baseball player get arrested? He stole third base.
What did one piece of tape say to the other? Let’s stick together.
What’s brown and sticky? A stick.
How does the rancher keep track of his cattle? With a cow-culator.
What do you call a shoe made out of a banana? A slipper.
How you fix a broken pumpkin? With a pumpkin patch.
Where do boats go when they’re sick? To the dock.
Can February March? No, but April May!
What do you call a fibbing cat? A lion.
Did you hear the rumor about butter? Well, I’m not going to go spreading it!
Where do you learn to make ice cream? Sundae school.
What’s a scarecrow’s favorite fruit? Straw-berries
Where do burgers go dancing? At the meatball.
What time do ducks wake up? At the quack of dawn.
Why was the broom late? It over-swept.
What kind of tree fits in your hand? A palm tree.
Where do books hide when they’re afraid? Under their covers.
How do trees get on the internet? They log in.
What does a painter do when he gets cold? Puts on another coat.
What did the calculator say to the pencil? You can count on me.
What has four wheels and flies? A garbage truck.
What do you call two ducks and a cow? Quackers and milk.
What do cows like to read? Cattle-logs.
How did the farmer fix his torn overalls? With a cabbage patch.
How much money does a skunk have? Just one scent.
What do you get when you cross an elephant and a fish? Swimming trunks.
What kind of cereal do leprechauns eat? Lucky Charms.
What do you call recently-married spiders? Newly-webs.
Where do crayons go on vacation? Color-ado.
What do you get when you cross a Smurf and a cow? Blue cheese.
What happens when ice cream gets angry? It has a meltdown.
What do you call a locomotive carrying bubble gum? A chew chew train.
How do you get a mouse to smile? Say cheese.
Why couldn’t the bike stand up on its own? It was too tired.
What do you call a sheep that knows karate? A lamb chop.
Why did the snowman buy a bag of carrots? He wanted to pick his nose.
What did the Dalmatian say after dinner? That hit the spot.
How do you know when a bike is thinking? You can see its wheels turning.
What does a librarian use to go fishing? A bookworm.
What did one leaf say to the other? I’m falling for you.
Where’s the one place you should never take your dog? A flea market.
How does Darth Vader like his bagels? On the dark side.
What do you call spaghetti in disguise? An impasta.
Why did the tailor get fired? He wasn’t a good fit.
Where do elephants store luggage? In a trunk.
Did you hear about the red and blue ships that collided? All the sailors were marooned.
My neighbor gave me a new roof for free. He said it was on the house.
Did you hear about the teenager who failed his driving test? He thought it was a crash course.
Where do surfers learn to surf? At boarding school.
A duck walks into a bar and buys everyone a round. He tells the bartender, Put it on my bill.
What has a spine but no bones? A book.
What do you call a wizard who’s good with ceramics? Harry Pottery.
Why did Marie Curie stop dating that guy? There was no chemistry.
Did you hear about the nurse who didn’t want to become a doctor? She didn’t have the patients.
Why did the tourist feel disappointed upon seeing the Liberty Bell? It wasn’t all it was cracked up to be.
How did Vikings communicate with one another? By Norse code.
How did Benjamin Franklin feel when he discovered electricity? He was shocked!
Which is the worst sport to play? Bad-minton.
Why don’t the other farm animals like playing basketball with pigs? They’re ball hogs.
How do ghosts stay in shape? They exorcise.
What do rabbits need after getting caught in the rain? A hare dryer.
Why did the coach put the frog in the outfield? He’s really good at catching flies.
What board game is popular in Prague? Czechers.
What kind of shoes does a lazy person wear? Loafers.
Why didn’t the invisible man go to the dance? He didn’t have any body to take.
Dad, did you get a haircut? No, I got them all cut!
What did one candle say to the other? Do you want to go out tonight?
Why did the bed wear a disguise? It was undercover.
What do you call a boomerang that doesn’t come back? A stick.
What do you call a monster with a high IQ? Frank-Einstein.
Why was the Incredible Hulk so good at gardening? He had a green thumb.
What kind of music does a boulder like? Rock ‘n’ roll.
Why did the elephant quit his job? He was working for peanuts.
What did the shovel say to the sand? I really dig you!
What are the least expensive type of teeth? Buck teeth.
What would happen if you threw all the books in the ocean? It would cause a title wave.
Why did the queen go to the dentist? To get crowns on her teeth.
What’s the best kind of music to listen to when fishing? Something catchy.
How did the pirate get his ship for so cheap? It was on sail.
Today my son asked me, Can I have a bookmark? I burst into tears — he’s 12 years old and still doesn’t know my name!
Why do dads take an extra pair of socks when they play golf? In case they get a hole in one.
What do you call a fish with no eyes? A fsh.
Why don’t seagulls fly over the bay? Because then they’d be bagels (bay gulls).
What comes once in a minute, twice in a moment but never in a thousand years? The letter M.
What’s the best kind of bird to work for at a construction company? A crane.
What did the T-Rex use to cut wood? A dino-saw.
I got fired from my job as a taxi driver. It turns out nobody thought I was fare.
What do you call a snake that loves building houses? A boa constructor.
Where do fish keep their money? In a river bank.
Why did the man put his money in the freezer? He wanted cold, hard cash.
When does it rain money? When there is a change in the weather.
Why don’t scientists trust atoms? Because they make up everything.
What do a tick and the Eiffel Tower have in common? They’re both Paris sites.
Why did the man get fired from the banana factory? He kept throwing away the bent ones.
Whoever stole my depression medication — I hope you’re happy now.
Why can’t a leopard hide? Because he’s always spotted.
What do you call two monkeys who share an Amazon account? Prime mates.
What do you call a penguin in the White House? Lost.
What do you call a kangaroo’s lazy joey? A pouch potato.
What did the llama say to his date? Want to go on a picnic? Alpaca lunch.
Did you hear that I’m reading a book about anti-gravity? It’s impossible to put down.
Which is faster, hot or cold? Hot, because you can catch a cold.
Which bear is the most condescending? A pan-duh.
What kind of noise does a witch’s vehicle make? Brrrroooom, brrroooom.
Singing in the shower is fun until you get soap in your mouth. Then it’s a soap opera.
I only know 25 letters of the alphabet. I don’t know y.
How does the moon cut his hair? Eclipse it.
What do you call a factory that makes OK products? A satisfactory.
What did the janitor say when he jumped out the closet? Supplies!
What did the buffalo say to his son when he dropped him off at school? Bison!
I can tolerate algebra, maybe even a little calculus, but geometry is where I draw the line.
Why do bees have sticky hair? Because they use a honeycomb.
What kind of music do chiropractors like? Hip pop.
What has five toes and isn’t your foot? My foot.
What did the cannibal choose as his last meal? Five Guys.
Me: Go to bed, the cows are already asleep in the field. Son: So what? Me: It’s pasture bedtime.
What do you call a Frenchman in sandals? Philippe Philoppe.
I bought the world’s worst thesaurus yesterday. Not only is it terrible, it’s terrible.
Why did the scarecrow get an award? Because he was outstanding in his field.
What do you get if you cross an angry sheep with a moody cow? An animal that’s in a baaaaad mooood.
Can a kangaroo jump higher than the Empire State Building? Of course! Buildings can’t jump.
What did the sink tell the toilet? You look flushed.
What happens when a snowman throws a tantrum? He has a meltdown.
My extra winter weight is finally gone. Now, I have spring rolls.
I just found out I’m colorblind. The news came out of the orange!
Did you hear that laughing too loudly is illegal in Hawaii? They only permit a-low-ha.
I hate my job — all I do is crush cans all day. It’s soda pressing.
Mom keeps asking why I have so much candy. She doesn’t know I always keep a few Twix up my sleeve.
I found a wooden shoe in my toilet — it was clogged.
If a pig loses its voice, does it become disgruntled?
I love dad jokes, but I don’t have kids, which makes me a Faux Pa.
I only know 25 letters of the alphabet — I just don’t know y.
My dream job is to clean mirrors, because I can really see myself doing that.
I lost 25% of my roof last night...oof.
I don’t trust stairs. They’re always up to something.
RIP, boiling water. You will be mist.
Two guys walked into a bar. The third guy ducked.
Two peanuts went walking down the street. One was assaulted.
I’m so good at sleeping that I can do it with my eyes closed!
I had a dream that I weighed less than a thousandth of a gram. I was like, 0mg.
Mom said I should do lunges to stay in shape. That would be a big step forward.
Time flies like an arrow. Fruit flies like a banana.
Every time I take my dog to the park, the ducks try to bite him. That’s what I get for buying a pure bread dog.
6:30 is my favorite time of day, hands down.
Whenever you get a bad sausage, it’s just the wurst.
My dog is a genius. I asked him, What’s two minus two? He said nothing.
I used to run a dating service for chickens, but I was struggling to make hens meet.
Mom texted me to say our Italian restaurant is out of pasta, and now we’re penneless.
Justice is a dish best served cold. If it were served warm, it would be justwater.
I used to hate facial hair, but then it grew on me.
Most people can’t tell the difference between entomology and etymology. I can’t find the words for how much this bugs me.
A magician was walking down the street — then he turned into a store.
We’re renovating the house, and the first floor is going great, but the second floor is another story.
I’m reading an anti-gravity book, and I just can’t put it down!
At first, I thought my chiropractor wasn’t any good, but now I stand corrected.
My toddler is refusing to nap. He’s guilty of resisting a rest.
I used to be able to play piano by ear, but now I have to use my hands.
I failed my calculus exam because I was sitting in the middle of identical twins — I couldn’t differentiate between them.
My boss asked me why I only get sick on work days. I said it must be my weekend immune system.
Every night, I have hard time remembering something, but then it dawns on me.
The wedding was so beautiful, even the cake was in tiers.
I can tolerate algebra, maybe even a little calculus but geometry is where I draw the line.
I was wondering why the baseball kept getting bigger and bigger. Then it hit me.
Have you heard about the new corduroy pillows — they’re making headlines!
My therapist told me I have problems expressing my emotions. Can’t say I’m surprised.
I was once a personal trainer, until I gave a too-weak notice.
I just paid $100 for a belt that doesn’t fit — what a huge waist!
I finally watched that documentary on clocks. It was about time.
Bigfoot is sometimes confused for Sasquatch — Yeti never complains.
Your mom and I let astrology get between us. It just Taurus apart.
A guy walked into a bar, and lost the limbo contest.
I wanted to eat a watch for lunch, but it was too time-consuming.
I ordered a chicken and an egg online. I’ll let you know what comes first.
It’s raining cats and dogs, so be careful not to step in a poodle.
I decided to sell the vacuum cleaner — it was just gathering dust!
My boss told me to have a good day, so I went home!
Mom says I have no sense of direction, so I packed my bags and right.
If money doesn’t grow on trees, then why do banks have branches?
Mom is mad at me because she asked me to sync her phone, so I threw it in the ocean.
I’d avoid the sushi if I were you — it’s a little fishy!
I can tell when you’re lying just by looking at you. I can also tell when you’re standing.
I was going to go on an expensive vacation with a classical pianist, but he was too baroque.
Mom asked me to put ketchup on the grocery list, and now I can’t read what else is on it.
Can anyone tell me what oblivious means, because I have no idea.
My friend couldn’t pay his water bill, so I sent him a get well soon card
Does anybody know where a dad can find a person to talk to and hang out with? Asking for a friend.
Lance isn’t that common a name these days, but in medieval times, they were called lance-a-lot.
After dinner Mom asked if I could clear the table. I needed a running start, but I made it.
I want to name my puppies Rolex and Timex so I can have watch dogs.
I love telling Dad jokes. Sometimes, he even laughs.
What does a baby computer call its father? Data!
What’s green and has wheels? Grass! I lied about the wheels.
Where do pirates get their hooks? Second hand stores!
Why are pupils are the last part of your body to stop working when you die? They dilate!
What do you call a line of dads waiting to get haircuts? The barberqueue!
What do you call a beehive with no exit? Unbelievable!
What did the doctor say to the panicked man who was afraid he was shrinking? Settle down — you’ll have to learn to be a little patient!
Why was 2019 afraid of 2020? Because they had a fight and 2021!
Why should you never brush your teeth with your left hand Because a toothbrush works better!
What do you call a rude cow? Beef jerky!
What’s the best thing about living in Switzerland? I don’t know, but the flag is a big plus!
Why are balloons so expensive? Inflation!
What is the most popular time for a dentist appointment? Tooth hurty!
Do you want to hear two short jokes and a long joke? Joke! Joke! Jooooooooooooooooke.
What do you call cheese that isn’t yours? Nacho cheese!
Why can’t you send a duck to space? Because the bill would be astronomical!
What side of a tree grows the most branches? The outside!
What happened when the world’s tongue-twister champion got arrested? They gave him a tough sentence.
Why did an old man fall in a well? Because he couldn’t see that well!
Did you hear about that person who was afraid of jumping a hurdle? They got over it!
What do you call a fish with no eye? A fsh.
What breed of dog can jump higher than a skyscraper? Any breed of dog! Skyscrapers can’t jump.
Why are elevator jokes so good? They work on many levels!
Why are peppers the best at archery? Because they habanero!
What state is known for its tiny beverages? Minnesota!
Why did the computer get mad at the printer? Because it didn’t like its toner voice.
What did the three-legged dog say when he walked into a saloon? I’m looking for the man who shot my paw.
What’s the best way to watch a fly-fishing tournament? Live stream it!
Why did the broom decide to go to bed? It was very sweepy!
Why are nurses always running out of red crayons? Because they often have to draw blood!
Did you hear about the square that got into a car accident? Yeah, now he’s a rect-angle!
What do you call an illegally parked frog? Toad!
How do you tell the difference between a bull and a cow? It is either one or the utter.
What’s red and smells like blue paint? Red paint!
Why can’t you ever run through a campsite? You can only ran — it’s always past tents!
Why was the woman afraid for the calendar? She said its days were numbered!
Why is it hard to understand volunteers? Because they make no cents!
What did the police officer say to his belly-button? You’re under a vest!
What’s the easiest way to burn 1,000 calories? Leave the pizza in the oven!
What do you call a hippie’s wife? Mississippi!
What’s the difference between a badly dressed kid on a bicycle and a well dressed kid on a tricycle? Attire!
What did the drummer call his twin daughters? Anna One, Anna Two!
Did you hear about the king who was exactly 12 inches tall? He was a great ruler!
What’s the difference between a hippo and a Zippo? One is very heavy, the other is a little lighter.
How do you cure a fear of a speed bump? You slowly get over it.
Why is the cow always smiling? It’s in a good mooood I guess!
When did they find water on the moon? When it was waning!
What do you call a boomerang that doesn’t come back? A stick!
Why is Peter Pan always flying? Because he Neverlands!
Why don’t astronomers like Orion’s Belt? It’s a big waist of space!
What did the photon say to the hotel bellhop? No luggage, I’m traveling light!
Why did the coffee go to the police? To report a mugging!
What’s the difference between a dad joke and a bad joke? The direction of the first letter.
I have a joke about putting in a light bulb, but I’m afraid I’ll screw it up.
I have a joke about chemistry, but I don’t think it’ll get a reaction.
I have a joke about banking, but I lost interest.
I have a joke about cows, but I don’t want to milk it.
I have a joke about kites, but it would just sail over your head.
I have a joke about scary math, but I’m 2² to say it.
I have a joke about construction, but I’m still working on it.
I have a joke about time travel, but you guys didn’t get it.
I have a joke about being an electrician, but it’s too shocking.
I have a joke about hunting for fossils, but you probably wouldn’t dig it.
I have a joke about a broken pencil, but it’s pointless.
I have a joke about the flu, but I hope you don’t get it.
I have a joke about statistics, but it’s not significant.
I have a joke about pizza, but it’s too cheesy.
I have a joke about immortality, and it never gets old.
I have a joke about paper, but it’s tearable.
I have a joke about trickle-down economics, but 99% of you will never get it.
I have a joke about drilling, but it’s boring.
I have a joke about being a rejected organ donor, but I just don’t have the guts to tell it.
I had a joke about canned juice, but I couldn’t concentrate.
I have a few jokes about retired people, but none of them work.
I have a joke about a broken clock, but it’s not the right time.
I have a joke about nepotism, but I’ll only give it to my kids.
I have a joke about butter, but I’m not going to spread it.
I have a joke about a roof, but it would just go over your head.
I have a joke about inferiority complexes, but it’s not very good.
I have a joke about procrastination, but I’ll tell it to you later.
Why does Marvel advertise The Hulk the most? Because he’s basically one big Banner!
What’s E.T. short for? Because he’s only got tiny legs!
What concert costs just 45 cents? 50 Cent featuring Nickelback!
What’s Forrest Gump’s email password? 1Forrest1
What does Jeff Bezos do before he goes to sleep? He puts his PJ-Amazon.
How do you follow Will Smith in the snow? You follow the fresh prints.
How does Darth Vader like his toast? On the dark side.
Why won’t Apple start making cars? They wouldn’t support windows.
What type of coordination was Whitney Houston most famous for? Hand eeeeyeeeeee!
What do you say when Dwayne Johnson buys something to cut with? Rock pay-for scissors.
To the person stole my laptop with my copy of Microsoft Office on it: I will find you. You have my Word!
To the person who stole my glasses: I will find you. I have contacts.
To the person who stole my place in line: I’m after you now.
To the person who stole my limbo stick: That was a new low.
To the person who stole my dictionary: I have no words.
To the person who stole my bed: I won’t rest until I find you.
To the person who stole my depression medication: I hope you’re happy now.
To the person who stole my case of energy drinks: I hope you can’t sleep at night.
To the person who stole my power steering: I just can’t handle it.
To the person who stole my diary and then died: My thoughts are with your family.
RIP boiling water, you will be mist.
I once wrote a song about a tortilla, but it’s more of a wrap.
A witch’s vehicle goes brrroom brrroom!
The waiter asked if I wanted a box for my leftovers, but I told him I’m not into fighting.
If you see a crime at an Apple store, are you an iWitness?
If the early bird catches the worm, I’ll sleep in until there are pancakes.
The wedding was so beautiful, even the cake was in tiers.
I used to be able to play the piano by ear, but now I have to use my hands.
Did Noah include termites on the ark?
I used to hate facial hair, but it grew on me.
Keep the dream alive, and hit the snooze button.
I tell dad jokes but I have no kids. I’m a faux pa.
I’m afraid of speed bumps, but I am slowly getting over it.
Some people think prison is one word, but to robbers, it’s the whole sentence.
I used to be addicted to soap, but I’m clean now.
Spring is here! I got so excited I wet my plants!
I poured root beer in a square glass. Now I just have beer.
I had a dream about being a muffler. I woke up exhausted.
Talk is cheap until you talk to a lawyer.
A pony with a cough is just a little horse.
It takes guts to be an organ donor.
To whoever stole my copy of Microsoft Office, I will find you. You have my Word!
How do celebrities stay cool? They have many fans.
What’s Forrest Gump’s Facebook password? 1forest1.
What did the fisherman say to the magician? Pick a cod, any cod.
What do you call a fake noodle? An impasta.
How do you organize a space party? You planet.
Did you know that milk is the fastest liquid on earth? It’s pasteurized before you can even see it.
What does a baby computer call his father? Data.
Why can’t a leopard hide? Because he’s always spotted.
How many tickles does it take to make an octopus laugh? 10 tickles.
What do you call an illegally parked frog? Toad.
Why are spiders so smart? They can find everything on the web.
It’s inappropriate to make a dad joke if you’re not a dad. It’s a faux pa.
Did you hear about the circus fire? It was in tents.
Can February March? No, but April May!
How do lawyers say goodbye? We’ll be suing ya!
Wanna hear a joke about paper? Never mind—it’s tearable.
What’s the best way to watch a fly fishing tournament? Live stream.
I could tell a joke about pizza, but it’s a little cheesy.
Every time I take my dog to the park, the ducks try to bite him. That’s what I get for buying a pure bread dog.
What is a funny mountain called? Hill-arious.
I wouldn’t buy anything with velcro. It’s a total rip-off.
What time did the man go to the dentist? Tooth hurt-y.
What kind of egg did the evil chicken lay? A deviled egg.
Which is faster, hot or cold? Hot, because you can catch a cold.
I made a pencil with two erasers. It was pointless.
How does a bee brush its hair? It uses a honeycomb.
How do you make a Kleenex dance? Put a little boogie in it!
What do you get from a pampered cow? Spoiled milk!
Where do baby cats learn to swim? The kitty pool.
How can you tell it’s a dogwood tree? From the bark.
What sound does the engine of a witch’s vehicle make? Broooom broooom!
What do you call a fish wearing a bow tie? Sofishticated.
What bone will a dog never eat? A trombone.
Sundays are always a little sad, but the day before is a sadder day.
Where do you learn to make a banana split? Sundae school.
How do you row a canoe filled with puppies? Bring out the doggy paddle.
Why is cold water so insecure? Because it’s never called hot.
I don’t trust stairs. They’re always up to something.
Why do bees have sticky hair? Because they use a honeycomb.
What did Tennessee? The same thing as Arkansas.
Why is it bad to iron your four-leaf clover? Because you shouldn’t press your luck.
What rock group has four men who don’t sing? Mount Rushmore.
Where do pirates buy hooks? The second hand store.
Why didn’t the skeleton go on the rollercoaster? It didn’t have the guts.
Why did the birds attack the dog? He was pure bread.
What did the nose tell the finger? Stop picking on me.
What do you call a sick lemon? Lemon-aid.
What gets wetter the more it dries? A towel.
What do you call a toothless bear? A gummy bear.
Why can’t your hand be 12 inches long? Because then it would be a foot.
What has four wheels and flies? A garbage truck.
Why are pigs so bad at sports? Because they always hog the ball.
Time flies like an arrow. Fruit flies like a banana.
How do moths swim? Using the butterfly stroke.
What’s an astronaut’s favorite part of a computer? The space bar.
I hit in the head with a soda can. Thankfully it was a soft drink.
What’s the name of my cheese? Nacho cheese.
Knock, knock. Who’s there? Cows go. Cows go who? No, cows go moo!
What’s the loudest pet you can own? A trumpet.
What did the buffalo say to his son when he dropped him off at school? Bison.
What does a pampered cow give? Spoiled milk.
I made a whopping six figures last year. I also was fired from the toy factory for being too slow.
Knock, knock. Who’s there? A little old lady. A little old lady who? Hey, you can yodel!
Why did the teddy bear skip dessert? She was stuffed.
What did the left eye say to the right? Something smells between us.
What do you call a singing laptop? A Dell.
What’s it called when a snowman throws a tantrum? A meltdown.
What did the scarecrow win an award for? He was outstanding in his field.
I don’t know much about the best things in Switzerland, but their flag is a big plus.
I used to hate facial hair, but then it grew on me.
I invented a pencil with an eraser on each end. There’s no point to it.
What do you call it when Batman skips church? Christian Bale.
Did you hear about the man who fell into an upholstery machine? He’s fully recovered.
Why are skeletons so calm? Because nothing gets under their skin.
What’s the astronaut’s favorite part of a computer? The spacebar.
What did one ocean say to the other ocean? Nothing, they just waved.
Did you hear about the power outlet who got into a fight with a power cord? He thought he could socket to him.
Why are elevator jokes so good? They work on so many levels.
Why did the nurse need a red pen? In case she needed to draw blood.
Do you know the story about the chicken that crossed the border? Me neither, I couldn’t follow it.
How can a leopard change his spots? By moving.
Don’t trust atoms. They make up everything!
What’s an astronaut’s favorite part of a computer? The space bar.
I’m afraid of the calendar. Its days are numbered.
Two guys walked into a bar. The third guy ducked.
My wife said I should do lunges to stay in shape. That would be a big step forward.
What did the zero say to the eight? That belt looks good on you.
I got carded at a liquor store, and my Blockbuster card accidentally fell out. The cashier said never mind.
How do trees get online? They just log on.
How does the moon cut his hair? Eclipse it.
Air used to be free at the gas station. Now it’s $1.50. You know why? Inflation.
When I was a kid, my mother told me I could be anyone I wanted to be. Turns out, identity theft is a crime.
I’ll call you later. Don’t call me later, call me Dad!
When does a joke become a dad joke? When it becomes apparent.
Which bear is the most condescending? A pan-duh.
What kind of drink can be bitter and sweet? Reali-tea.
Why do dads take an extra pair of socks when they golfing? In case they get a hole in one!
Singing in the shower is fun until you get soap in your mouth. Then it’s a soap opera.
Where do fruits go on vacation? Pear-is.
Why do melons have weddings? Because they cantaloupe.
What kind of cars do eggs drive? Yolkswagens.
Why did the picture get arrested? It got framed.
Why do M&Ms go to school? Because they want to be a Smartie.
Knock knock. Who’s there? Tank. Tank who? You’re welcome.
How do you protect a bagel? Lox it up!
I like telling Dad jokes. Sometimes he laughs!
Why did the stadium get hot after the game? All of the fans left.
Why shouldn’t you enter into a contract with Wolverine? Because of his retractable clause.
What kind of coffee does a vampire drink? De-coffin-ated.
How do you keep a skunk from smelling? Hold its nose!
What do you call a fish with two knees? A two-knee fish!
Why can’t you tell a taco a secret? They tend to spill the beans! %%Cinco De Mayo
Dogs can’t operate MRI machines. But catscan.
I wondered why the frisbee kept getting bigger and bigger. Then it hit me.
Why did the coach go to the bank? To get his quarter back.
Why do dads take an extra pair of socks when they golfing? In case they get a hole in one!
Singing in the shower is fun until you get soap in your mouth. Then it’s a soap opera.
Where do fruits go on vacation? Pear-is.
I was wondering why the ball kept getting bigger and bigger… // And then it hit me.
Why do melons have weddings? Because they cantaloupe.
What kind of cars do eggs drive? Yolkswagens.
Every time I take my dog to the park, the ducks try to bite him. That’s what I get for buying a pure bread dog.
Why does Snoop Dogg always carry an umbrella? Fo’ Drizzle.
Why did the gym close down? It just didn’t work out.
Two artists had an art contest. It ended in a draw.
Where are average things manufactured? The Satisfactory.
Want to hear a joke about construction? I’m still working on it.
What did one hat say to the other? Wait here, I’m going on ahead!
What cars do eggs drive? A Yolkswagen.
What does a baby computer call his father? Data.
After an unsuccessful harvest, why did the farmer decide to try a career in music? Because he had a ton of sick beets.
I only seem to get sick on weekdays. I must have a weekend immune system.
My friend was showing me his tool shed and pointed to a ladder. That’s my stepladder. he said. I never knew my real ladder.
What do you call a Frenchman wearing sandals? Philippe Flop.
Why is it so cheap to throw a party at a haunted house? Because the ghosts bring all the boos.
I don’t get why Marvel doesn’t use the Hulk to advertise more. He’s basically one big Banner.
What brand of underwear do scientists wear? Kelvin Klein.
Which days are the strongest? Saturday and Sunday. The rest are weekdays.
I just found out I’m colorblind. The news came out of the purple!
Did you know your pupils are the last part to stop working when you die? They dilate.
My wife asked me the other day where I got so much candy. I said, I always have a few Twix up my sleeve.
How do cows stay up to date? They read the Moo-spaper.
What’s the difference between a well-dressed man on a unicycle and a poorly-dressed man on a bicycle? Attire.
I hate my job—all I do is crush cans all day. It’s soda pressing.
Where do pirates get their hooks? Second hand stores.
Of all the inventions of the last 100 years, the dry erase board has to be the most remarkable.
In America, using the metric system can get you in legal trouble.
What do you call a line of men waiting to get haircuts? A barberqueue.
In fact, if you sneer at any other method of measuring liquids, you may be held in contempt of quart.
Who were the greenest Presidents in US history? The bushes.
My hotel tried to charge me ten dollars extra for air conditioning. That wasn’t cool.
What do you call a beehive without an exit? Unbelievable.
If I ever find the doctor who screwed up my limb replacement surgery…I’ll kill him with my bear hands.
Did you know that the first french fries weren’t cooked in France? They were cooked in Greece.
This morning, Siri said, Don’t call me Shirley. I accidentally left my phone in Airplane mode.
It’s easy to convince ladies not to eat Tide Pods, but harder to deter gents.
I asked my date to meet me at the gym but she never showed up. I guess the two of us aren’t going to work out.
How do you find Will Smith in a snowstorm? You look for fresh prints.
The difference between a numerator and a denominator is a short line. Only a fraction of people will understand this
I found a wooden shoe in my toilet today. It was clogged.
I just broke up with my mathematician girlfriend. She was obsessed with an X.
I can’t take my dog to the pond anymore because the ducks keep attacking him. That’s what I get for buying a pure bread dog.
To whoever stole my copy of Microsoft Office, I will find you. You have my Word.
What’s Forrest Gump’s password? 1forrest1.
I used to run a dating service for chickens. But I was struggling to make hens meet.
If prisoners could take their own mug shots…They’d be called cellfies.
Have you heard about those new corduroy pillows? They’re making headlines.
If a pig loses its voice…does it become disgruntled?
Wanna hear a joke about paper? Never mind. It’s tearable.
A panic-stricken man explained to his doctor, You have to help me, I think I’m shrinking. Now settle down, the doctor calmly told him. You’ll just have to learn to be a little patient.
What do you call a bundle of hay in a church? Christian Bale.
A ship carrying red paint and a ship carrying blue paint collide in the middle of the ocean. Both crews were marooned.
What is a guitar player’s favorite Italian food? Strum-boli.
How does cereal pay its bills? With Chex.
Have you heard about the restaurant on the moon? Great food, no atmosphere.
I don’t trust stairs. They’re always up to something.
People in Athens rarely get up before sunrise. Dawn is tough on Greece.
Why’d the alternate universe Spider-Man do so well on his driving test? He’s an excellent parallel Parker.
Never date a tennis player. Love means nothing to them.
What’s a lawyer’s favorite drink? Subpoena colada.
What did Yoda say when he saw himself in 4K? HDMI.
What do you call a wizard who’s really bad at football? Fumbledore.
How do nonbinary people hurt each other? They slash them. (They/them)
I used to hate facial hair, but then it grew on me.
What’s blue and not very heavy? Light blue.
I don’t get why bakers aren’t wealthier. They make so much dough.
I asked my wife if I was the only one she slept with. She said yes—the others were 7’s and 8’s.
How do you make a tissue dance? You put a little boogie in it.
How do flat-earthers travel? On a plane.
I ordered a chicken and an egg from Amazon. I’ll let you know.
Imagine if you walked into a bar and there was a long line of people waiting to take a swing at you. That’s the punch line.
My wife left me because of my obsession with pasta. I’m feeling cannelloni right now.
What’s an astronaut’s favorite part of the computer? The Space Bar.
I was playing chess with my friend and he said, Let’s make this interesting. So we stopped playing chess.
I was in a job interview the other day and they asked if I could perform under pressure. I said no, but I could perform Bohemian Rhapsody.
Why didn’t the vampire attack Taylor Swift? She had bad blood.
Today I’m attaching a light to the ceiling, but I’m afraid I’ll probably screw it up.
I hate it when people say age is only a number. Age is clearly a word.
I can’t take my dog to the pond anymore because the ducks keep attacking him. That’s what I get for buying a pure bread dog.
Someone complimented my parking today! They left a sweet note on my windshield that said parking fine.
I was excited to hear Apple might start selling its own cars until I learned they wouldn’t support windows.
I just applied for a job down at the diner. I told them I really bring a lot to the table.
Cop: I’m arresting you for downloading the entire Wikipedia. Man: Wait! I can explain everything!
My friend couldn’t afford to pay his bill, so I sent him a Get Well Soon card.
I’m Buzz Aldrin, second man to step on the moon. Neil before me.
Why was 2019 afraid of 2020? Because they had a fight and 2021.
Did you hear Bruce Springsteen changed the lyrics to one of his songs? What’s he going to change next—his hair? His clothes? His face?
This year’s Fibonacci convention is going to be really special. Apparently it’s as big as the last two put together.
An apple a day keeps the doctor away. At least it does if you throw it hard enough.
I’m addicted to collecting vintage Beatles albums. I need Help.
In 2017 I didn’t do a marathon. I didn’t do one in 2018, 2019, or 2020, either. This is a running joke.
Not to brag but I made six figures last year. I was also named worst employee at the toy factory.
Ever since we started quarantining, I’ve only been telling inside jokes.
If you’re feeling depressed, try drinking a gallon of water before you go to sleep. It’ll give you a reason to get out of bed in the morning.
My landlord told me we need to talk about the heating bill. Sure, I said. My door is always open.
I built a model of Mount Everest and my son asked if it was to scale. No, I said. It’s to look at.
What has five toes and isn’t your foot? My foot.
My friend claims he glued himself to his autobiography. I don’t believe him, but that’s his story and he’s sticking to it.
When I was a kid, my mother told me I could be anyone I wanted to be. Turns out, identity theft is a crime.
What’s brown and sticky? A stick.
My doctor told me I was going deaf. The news was hard for me to hear.
A century ago, two brothers decided it was possible to fly. And as you can see, they were Wright.
I’m reading a horror story in braille. Something bad is going to happen, I can just feel it.
Anyone looking to buy a Delorean? Good shape, good mileage. Only driven from time to time
During my calculus test, I had to sit between identical twins. It was hard to differentiate between them.
Does anybody know where a guy can find a person to hang out with, talk to, and enjoy spending time with? I’m just asking for a friend.
Why did the Invisible Man turn down a job offer? He couldn’t see himself doing it.
When I die, I want to be cremated. It’s my last chance to have a smokin’ hot body.
Just say NO to drugs! Well, if I’m talking to drugs, I probably already said yes.
I once saw a one-handed man in a second-hand store. I told him, I don’t think they have what you’re looking for, sir.
What do you call a sad cup of coffee? Depresso.
What did one monocle say to the other monocle? Let’s get together and make a spectacle of ourselves.
How come the Hulk doesn’t lose his pants when he transforms? The experiment altered his jeans.
I didn’t want to believe that my dad was stealing from his job as a traffic cop, but when I got home, all the signs were there.
I just spent $300 on a limo and learned it doesn’t come with a driver. I can’t believe I have nothing to chauffer it.
What’s green and has wheels? Grass. I lied about the wheels.
I have a joke about trickle down economics. But 99% of you will never get it.
Just got back from a job interview where I was asked if I could perform under pressure. I said I wasn’t too sure about that but I could do a wicked Bohemian Rhapsody.
What’s the best thing about living in Switzerland? I don’t know, but the flag is a big plus.
At the job interview, they asked me, Where do you see yourself in five years? I told him, I think we’ll still be using mirrors in five years.
A buddy asked how many fish I caught. I told him it’s not polite to fish and tell.
How many clickbait articles does it take to change a lightbulb? The answer will shock you!
How do you make a water bed bouncier? Add spring water.
I always knock on the fridge door before opening it, just in case there’s a salad dressing.
Where do dads store their dad jokes? In the dad-a-base.
What kind of fruit do ghosts like? Boo-berries. %%Halloween
I tried to start a professional hide and seek team, but it didn’t work out. Turns out, good players are hard to find.
Women should not have children after 36—really, 36 children is enough.
What happens when frogs park illegally? They get toad.
Lance isn’t that common a name these days, but in medieval times, they were called lance-a-lot.
I had an appointment to see my psychic next week, but she just called to cancel.
She said I won’t be able to make it.
I used to be addicted to soap, but I’m clean now.
I wanted my kids to watch the orchestra, but I had to turn it off—too much sax and violins.
A cop started crying while he was writing me a ticket. I asked him why and he said, It’s a moving violation.
Swords will never go obsolete. They’re cutting edge technology.
I asked the IT guy, How do you make a Motherboard? He said, I tell her about my job.
What do you call it when James Bond takes a bath? Bubble 07.
30 percent of pet owners let their pets sleep in their bed. I tried it and my goldfish died.
What is the difference between a literalist and a kleptomaniac?
I just found out Albert Einstein existed. My whole life I thought he was a theoretical physicist.A comma. A literalist takes everything literally. A kleptomaniac takes everything, literally.
You used to be able to get air for free at gas stations, but now it’s a $1. That’s inflation for you.
My dad was born a conjoined twin, but separated at birth. So I have an uncle, once removed.
Why is it a bad idea to eat a clock? Because it’s so time-consuming.
I went to a smoke shop only to discover it’d been replaced by an apparel store. Clothes, but no cigar.
Why should you never brush your teeth with your left hand? Because a toothbrush works better.
My grief counselor died the other day. He was so good at his job, I don’t even care.
Give a man a plane ticket and he flies for the day. Push him out of the plane at 3,000 feet and he’ll fly for the rest of his life.
As I get older, I remember all the people I lost along the way. Maybe a career as a tour guide was not the right choice.
I was reading a great book about an immortal dog the other day. It was impossible to put down.
What do you call someone who refuses to fart in public? A private tutor.
I just read that someone in London gets stabbed every 52 seconds. Poor bastard.
They say that breakfast is the most important meal of the day. Well, not if it’s poisoned. Then the antidote becomes the most important.
The guy who stole my diary just died. My thoughts are with his family.
Do you know the last thing my grandfather said to me before he kicked the bucket? Grandson, watch how far I can kick this bucket.
If you donate a kidney, everybody loves you and you’re a total hero. But try donating five kidneys and suddenly everyone is yelling and the police get called.
I have a fish that can breakdance. Only for ten seconds though, and only once.
My friend said that if he went off a cliff, it would be on his own accord. It’s a good thing he drives a Civic.
In my free time, I like to help blind people. Verb, not adjective.
A doctor walks into a room with a dying patient and tells him, I’m sorry, but you only have ten left. The patient asks him, Ten what, Doc? Hours? Days? Weeks? The doctor calmly looks at him and says, Nine.
I like to spend my weekends playing chess with elderly men in the park. But it’s becoming more difficult. You try finding exactly32 old guys.
What do you call bears with no ears? B.
What’s the difference between a wizard who raises the undead and a sexy vampire? One is a necromancer and the other is a neck romancer.
A man walks into a magic forest and tries to cut down a talking tree. You can’t cut me down, the tree complains. I’m a talking tree! The man responds, You may be a talking tree, but you will dialogue.
I heard Sony’s coming out with a new console during the pandemic...It’s called the Plaguestation 5.
When my uncle Frank died, he wanted his remains to be buried in his favorite beer mug. His last wish was to be Frank in Stein.
A man walks into a bar. The bartender asks, What do you want? The man says, Oh, just some fruit punch. The bartender sighs and shakes his head, If you want punch, you’re gonna have to wait in line. The man looks around, but there is no punchline.
What’s worse than biting into an apple and finding a worm? Biting into an apple and finding half a worm.
I just got my doctor’s test results and I’m really upset. Turns out, I’m not gonna be a doctor.
My wife and I have decided not to have kids. The kids are taking it pretty badly.
When does a joke become a dad joke? When it becomes apparent.
My daughter just shrieked at me, Daaaaaad, you haven’t listened to a word I’ve said, have you? What an odd way to begin a conversation.
I have a great joke about nepotism. But I’ll only tell it to my kids.
Dad, can you explain to me what a solar eclipse is? No sun.
What happened when the ten-year-old cannibal spilled his soup? His mother gave him an earful.
I’d like to have kids one day. I don’t think I could stand them any longer than that, though.
What did the buffalo say to his son when he dropped him off at school? Bison.
I wonder what my parents did to fight boredom before the internet. I asked my eighteen brothers and sisters but they didn’t have any idea either.
My parents raised me as an only child. Which really annoyed my younger brother.
I tell dad jokes but I have no kids. I’m a faux pa!
A kid decided to burn his house down. His dad watched, tears in his eyes. He put his arm around the mom and said, That’s arson.
Today I decided to go visit my childhood home. I asked the residents if I could come inside because I was feeling nostalgic, but they refused and slammed the door on my face. My parents are the worst.
What’s your name, son? The principal asked his student. The kid replied, D-d-d-dav-dav-david, sir. Do you have a stutter? the principal asked. The student answered, No sir, my dad has a stutter but the guy who registered my name was a real jerk.
Concerned that his son was spending too much time on video games, a dad told him, When Abe Lincoln was your age, he was studying books by the light of the fireplace. Oh yeah? the son retorts. Well, when Abe Lincoln was your age, he was President of the United States.
A father tells his son that he was adopted. I want to meet my biological parents, the son demands. We are your biological parents, the father responds. Now pack up, the new ones will pick you up in twenty minutes.
A son tells his father, I have an imaginary girlfriend. The father sighs and says, You know, you could do better. Thanks Dad, the son says. That means a lot. The father shakes his head and goes, I was talking to your girlfriend.
Yesterday, I was washing the car with my son. He said, Dad, can’t you just use a sponge?
My dad died because he couldn’t remember his blood type. He kept insisting we be positive, but it’s just so hard without him.
I tried to explain to my 4-year-old son that it’s perfectly normal to accidentally poop your pants. But he’s still making fun of me.
I wasn’t close to my father when he died. Which is lucky because he stepped on a landmine.
April showers bring May flowers, but what do May flowers bring? Pilgrims.
What do you call a fake noodle? An Impasta.
How do you make a tissue dance? Put a little boogie in it.
What is a funny mountain called? Hill-arious.
What do you call a song about a tortilla? A wrap.
What’s Forrest Gump’s password? 1forrest1.
Where do pirates buy hooks? The second hand store.
The child refused to nap. She was found guilty of resisting a rest.
Why did the tomato blush? It saw the salad dressing!
Why is it bad to iron a four leaf clover? Because you should never press your luck.
What did one hat say to the other? Wait here, I’m going on ahead!
What keys unlock a banana? Mon-keys.
What is a fancy fish called? So-fish-ticated.
What’s blue and doesn’t weigh much? Light blue.
Where do you learn to make a banana split? Sundae school.
What happened to the frog that parked illegally? It got toad.
What type of bear is toothless? A gummy bear.
What cars do eggs drive? A Yolkswagen.
Why didn’t the skeleton go on the rollercoaster? It didn’t have the guts.
What did the cereal bring to the bank? Chex.
How does the moon style his hair? Eclipse it.
Why did the birds attack the dog? He was pure bread.
What did one wall say to the other? Let’s meet at the corner.
Why couldn’t the bicycle stand up alone? Because it was two tired.
How do you make seven even? Take away the s.
What’s it called when a snowman throws a tantrum? A meltdown.
What did the scarecrow win an award for? He was outstanding in his field.
What cars do sheep drive? Lamborghinis.
How do cows learn about current events? They read the moo-spaper.
How do you make a water bed bouncier? Fill it with Poland Spring water.
I have a joke about construction, but I’m still working on it.
At least I know I can always count on my fingers.
I just gave my too weak notice at the gym.
I bought Velcro sneakers, but they were a total rip-off!
My dentist appointment is at tooth hurt-y.
Apparently it was the fridge shrinking my clothes…not the dryer.
Goodbye boiling water, you will be mist.
All the fruits go on vacation in Pear-is.
The dry-erase board is the most remarkable invention.
I brought an egg to a comedy show and he cracked up.
It takes a lot of guts to be an organ donor.
That ghost was such a bad liar…I could see right through him! %%Halloween
The football coach went to the bank to get his quarterback.
Spiders are so smart, they know everything on the web. %%Halloween
I used to have a fear of speed bumps, but I’m slowly getting over it.
I had to get a neck brace last year and I haven’t looked back since.
That circus fire was in tents.
I don’t want to be friends with Dracula anymore, he’s such a pain in the neck!
It was easy to stop women from eating Tide Pods, but I couldn’t deter gents.
A joke becomes a dad joke once it is apparent.
I don’t know much about the best things in Switzerland, but their flag is a big plus.
That wedding was so emotional, even the cake was in tiers.
Everyone’s sharing the rumor about butter, but I’m not about to spread it.
I told a joke about chemistry, but it didn’t get a reaction.
I’m a big dreamer, so I always hit the snooze button.
I saw the Apple store get robbed…I guess that makes me an iWitness.
That car seems nice, but the muffler looks exhausted.
The ghost told me he’d bring the boos to the party tonight. %%Halloween
I used to hate facial hair, but then it grew on me.
That vampire should see a doctor…he’s always coffin. %%Halloween
I’m following the seafood diet. I see food, then I eat it.
Why was 6 afraid of 7? Because 7 ate 9.
Dogs are not allowed to operate an MRI machine, but catscan!
Don’t eat my cheese, that’s nacho cheese! %%Cinco De Mayo
What computer is a singer? A Dell.
My boss wished me a good day, so I went back home.
Why do nurses always take the red crayons? They have to draw a lot of blood.
I had a clock for breakfast. It was super time-consuming.
What did one monocle say to the other monocle? Let’s meet up and make a spectacle of ourselves.
It’s painful to say this, but I have a bad sore throat.
What’s the least spoken language? Sign language.
A cheese factory exploded downtown. Da brie is all over the streets!
I’m so good at napping that I can do it in my sleep!
I only know 25 letters of the alphabet. I don’t know y.
What did one DNA molecule say to the other DNA molecule? How do these genes look on me?
Don’t go in the grass without armor! It’s full of blades!
Why did the invisible man decline the job offer? He couldn’t see himself doing it.
How much money is it to park Santa’s sleigh? Nothing. It’s on the house.
I’m so bored at work because all I do is crush cans all day. It’s soda pressing.
What does a buffalo say goodbye to his son? Bison.
3.14% of sailors are considered pi-rates.
What animal is the worst at hide-and-seek? A leopard because he’s always spotted.
What do you call someone who doesn’t have a nose or body? Nobody knows.
What does garlic do before it showers? Takes its cloves off.
Why did the dog float in the water? He was a good buoy.
I went to the restaurant on the moon. The food was delicious, but there was no atmosphere.
I invented a pencil with an eraser on each end. There’s no point to it.
What has five toes, a heel, and isn’t your foot? My foot.
Why didn’t Han Solo like his burger? It was too Chewie.
What’s the astronaut’s favorite part of a computer? The spacebar.
If you spell the words absolutely nothing backward, you get gnihton yletulosba, which ironically means…absolutely nothing.
I had a joke about boxing, but I forgot the punchline.
The farmers lost all their crops and decided to try a career in music instead. They just had too many sick beets.
I once was addicted to soap, but I’m all clean now.
The saying goes, An apple a day keeps the doctor away, but they keep calling me for my annual checkup.
I’ll never trust atoms. They make up everything!
I have a really funny joke about trickle-down economics, but there’s no use in telling it because 99% of you will never get it.
I didn’t understand why the frisbee kept getting bigger. Then it hit me.
I made a whopping six figures last year. I also was fired from the toy factory for being too slow.
A guy walked into a bar…then he was disqualified from the limbo contest.
I got an anonymous compliment about my parking skills today. It said, Parking fine.
The calendar’s days are numbered. I’ll start planning the funeral.
I shouldn’t have poured my root beer into a square glass. I hate beer!
I used to fill my tires for free, but now it costs a dollar. I guess that’s the inflation everyone’s talking about.
I’m such a morning person that I don’t even need an alarm clock. That and I drink a gallon of water before I go to bed.
What came first, the chicken or the egg? I just ordered both on Amazon, so I’ll let you know.
I’m the best at putting leaves in boiling water. It’s my special tea.
When I was younger, my parents told me I can be anyone I dreamed of becoming. Then I learned the hard way that identity theft is a crime.
Taylor Swift is immune to vampires. They know she has bad blood.
The bartender broke up with her boyfriend, but he convinced her to give him one more shot.
Did you hear about the new corduroy pillowcases? They’re making headlines.
If the early bird catches the worm, call me a night owl because I prefer pancakes.
The waiter asked if I wanted a box for my leftovers, but I told him I’m not into fighting.
I accidentally took out my Blockbuster card at the bar. The bouncer said never mind.
In a job interview, they asked me if I can perform under pressure. I told them I don’t know the lyrics.
This guy was fired for always sweeping girls off their feet. He was a super-aggressive janitor.
When two vegetarians get in a fight, is it still called beef?
I heard that 5/4 of people are bad at fractions.
I’m always getting sick during the week. I think I have a weekend immune system.
Did you hear the joke about déjà vu? Did you hear the joke about déjà vu?
Can a kangaroo jump higher than our house? Of course it can, a house can’t jump!
Why does Peter Pan always fly? He Neverlands.
What do you write on a rabbit’s birthday card? Hoppy Birthday!
Where do sick boats go to get better? The boat doc.
How does a banana answer a phone call? Yellow!
If it’s raining cats and dogs, make sure you don’t step in a poodle!
How does a bee brush its hair? It uses a honeycomb.
What animal is dishonest? A lion.
What has four wheels and flies? A garbage truck.
Where do young trees learn math? Elementree school.
What’s a lazy kangaroo called? A pouch potato.
The finger was put in detention for always picking on the nose.
Mount Rushmore is the only rock group that doesn’t sing or play musical instruments.
What do tacos say in church? Lettuce pray! %%Cinco De Mayo
What do Santa’s elves learn in Kindergarten? The elphabet.
What’s the difference between a crocodile and an alligator? You will see one in a while and one later.
What does a pampered cow make? Spoiled milk.
What’s the Easter Bunny’s favorite music genre? Hip-hop.
What is a pony with a sore throat called? A little hoarse.
Where do baby cats swim? The kitty pool.
How do astronauts organize a trip? They planet.
I have a joke about pizza, but it’s really cheesy.
What do clouds wear? Thunderwear.
What’s brown and sticky? A stick.
What game are tornadoes the best at? Twister.
Why do giants sound so smart? They use big words!
If a squirrel seems to like you, you must be a bit nutty.
What’s a ghost’s favorite fruit? Boo-berries! %%Halloween
What sound does the engine of a witch’s vehicle make? Broooom broooom!
What’s orange and sounds just like a parrot? A carrot.
Did you hear about the circus fire? It was in tents!
How do you catch a squirrel? Climb a tree and act like a nut!
Did you hear about the guy who invented Lifesavers? They say he made a mint!
I told my wife she should embrace her mistakes. She gave me a hug.
Why don’t eggs tell jokes? They might crack up!
What did the big flower say to the little flower? Hi, bud!
I went to buy some camouflage pants, but I couldn’t find any.
What did the grape say when it got stepped on? Nothing, it just let out a little wine.
I used to have a job at a calendar factory, but I got fired because I took a couple of days off.
What do you call a snowman with a six-pack? An abdominal snowman!
Why don’t skeletons fight each other? They don’t have the guts!
Did you hear about the restaurant on the moon? Great food, no atmosphere!
What did one wall say to the other wall? I’ll meet you at the corner!
Why did the math book look sad? Because it had too many problems!
What did one hat say to the other hat? You stay here, I’ll go on ahead!
Why did the coffee file a police report? It got mugged!
I was going to tell you a joke about time travel, but you didn’t like it.
I used to be a baker, but I couldn’t make enough dough.
Did you hear about the guy who got hit in the head with a can of soda? He was lucky it was a soft drink.
I’m writing a book about glue, but I’m stuck on the first chapter.
What did one plate whisper to the other plate? Dinner is on me.
Why did the golfer bring two pairs of pants? In case he got a hole in one.
Two sheep walk into a—baaaa.
Stop looking for the perfect match; use a lighter.
Try the seafood diet—you see food, then you eat it.
Did you hear the rumor about butter? Well, I’m not going to go spreading it!
What’s Forrest Gump’s password? 1forrest1
What state is known for its small drinks? Minnesota.
What does a nosey pepper do? It gets jalapeño business.
If two vegetarians get in an argument, is it still called beef?
I have a clean conscious—it’s never been used.
I love telling Dad jokes. Sometimes, he even laughs.
Can a kangaroo jump higher than a house? Of course, houses can’t jump.
Why did the scarecrow win an award? He was outstanding in his field.
What concert would cost only 45 cents? 50 Cent featuring Nickelback!
How many telemarketers does it take to change a light bulb? Only one, but he has to do it during dinner.
What are the strongest days of the week? Saturday and Sunday. All the others are weekdays.
What did the seal with one fin say to the shark? If seal is broken, do not consume.
How do you deal with a fear of speed bumps? You slowly get over it.
How do you measure the mass of an influencer’s following? By Instagrams!
How do you stop a bull from charging? Cancel its credit card.
Am I the only man my wife has ever dated? Unfortunately, yes, she said the others were all nines or tens!
What’s the difference between a man’s wallet before and after kids? There are pictures where the money used to be.
I haven’t spoken to my wife in four years. I thought it would be rude to interrupt her!
I wish my gray hair started in Las Vegas because what happens in Vegas, stays in Vegas.
How do you follow Will Smith in the Mud? Follow the fresh prints.
My kid is blaming me for ruining their birthday. That’s ridiculous, I didn’t even know it was today!
My kid gave me a ’World’s Best Dad’ mug. At least she inherited my sense of humor.
When a toddler reaches the why? stage, it’s like opening a bottle of champagne—once it’s uncorked, there’s no going back.
What’s 90 degrees but covered with ice? The North and South Poles.
What happened when the blue ship and the red ship collided at sea? Their crews were marooned.
What’s the difference between the bird flu and the swine flu? One requires tweetment and the other an oinkment.
What do you call a line of men waiting to get haircuts? A barberqueue.
Why do seagulls fly over the sea? If they flew over the bay, they would be bagels.
I’m thinking I should do lunges to stay in shape. That would be a big step forward.
What did the baby corn say to the mama corn? Where’s popcorn?
What vegetable is cool, but not that cool? Radish.
What do you call two monkeys who share an Amazon Prime account? Prime mates.
You can’t spell par entry without try.
What do you call a beehive without an exit? Un-bee-lievable.
Why did the football coach go to the bank? To get his quarter back.
Why can’t a leopard hide? He’s always spotted.
Air used to be free at the gas station, now it costs 2.50. You want to know why? Inflation.
I tried to get a smart car the other day but they sold out too fast. Why? I guess I’m just a bit slow.
Did you hear about the claustrophobic astronaut? He just wanted a bit more space.
Why did the orange lose the race? It ran out of juice.
How you fix a broken pumpkin? With a pumpkin patch.
Why are fish so smart? They live in schools!
What’s the best thing about Switzerland? I don’t know, but the flag is a big plus.
Why did the man fall down the well? Because he couldn’t see that well!
Why do peppers make such good archers? Because they habanero.
What did the sink tell the toilet? You look flushed!
Where do boats go when they’re sick? To the dock.
What has ears but cannot hear? A cornfield!
Can February March? No, but April May!
Why was 6 afraid of 7? Because 7 ate nine!
I’m so good at sleeping that I do it with my eyes closed.
What do you call a pencil with two erasers? Pointless.
Did you hear the one about the roof? Never mind, it’s over your head.
What’s brown and sticky? A stick.
I hated facial hair but then it grew on me.
It really takes guts to be an organ donor.
What did the plumber say to the singer? Nice pipes.
I was going to tell a time-traveling joke, but you guys didn’t like it.
I ordered a chicken and an egg online. I’ll let you know.
I’m reading an anti-gravity book. I can’t put it down!
I’d avoid the sushi if I were you. It’s a little fishy!
What do houses wear? An address.
What did the two pieces of bread say on their wedding day? It was loaf at first sight.
What kind of shoes does a lazy person wear? Loafers.
What did the ocean say to the beach? Nothing, it just waved.
What happens when a snowman throws a tantrum? He has a meltdown.
Why’d the fisherman order the halibut? Just for the halibut!
Why is Peter Pan always flying? Because he Neverlands.
What do you call a sleeping bull? A bulldozer.
How do you throw a party in outer space? You planet.
Why was the broom late to class? It over-swept.
How do you make an octopus laugh? With ten-tickles!
What do you say to a rabbit on its birthday? Hoppy Birthday!
What type of tree fits in your hand? A palm tree.
Why couldn’t the bicycle stand up by itself? It was two tired!
Wanna hear a joke about construction? I’m still workin’ on it!
What do you call a fake noodle? An impasta.
How does a lawyer say goodbye? I’ll be suing ya!
You can’t trust atoms. They make up everything!
What made the tomato blush? It saw the salad dressing.
Can I dive in this pool? It deep-ends.
What did the buffalo say to its son when he left? Bison!
Why do vampires always seem sick? They’re coffin. %%Halloween
What musical instrument do you find in the bathroom? A tuba toothpaste!
Which state has the most streets? Rhode Island.
How do astronomers organize a party? They planet.
Why do bees have sticky hair? Because they use a honeycomb.
Why do melons have weddings? They cantaloupe!
What did the police officer say to her belly button? You’re under a vest!
What do you call a fibbing cat? A lion.
If a child refuses to nap, are they guilty of resisting a rest?
Did you hear about the outlet who got in a fight with the power cord? He thought he could socket to him.
What do you call a fancy fish? So-fish-ticated.
If April showers bring May flowers, what do May flowers bring? Pilgrims.
How do you make 7 even? You take away the s.
What kind of cars do eggs drive? Yolkswagens.
Where do math teachers go on vacation? Times Square.
Why was the stadium so hot after the game? Because all the fans left.
The coach went to the bank to get his quarterback.
I asked my dog what’s two minus two. He said nothing.
The first thing Santa’s elves learn in school is their elf-abet. %%Christmas
Ghosts are bad liars because you can see right through them. %%Halloween
Shouldn’t the roof of your mouth actually be called the ceiling?
All vampires keep their money in a special place—the blood bank.
The pony couldn’t sing because it was a little horse.
RIP boiling water, you will be mist.
I told my doctor I heard buzzing, but she said it’s just a bug that’s going around.
I ate a clock the other day. It was very time consuming.
I once wrote a song about a tortilla, but it’s more of a wrap.
You can tell it’s a dogwood tree from its bark.
When does a joke turn into a dad joke? When it becomes apparent.
They say that 3/2 people are bad at fractions.
Dogs can’t operate MRI machines but catscan.
A witch’s vehicle goes brrrroom brrrroom!
I’m worried for the calendar because its days are numbered.
Dear Math, it’s time to grow up and solve your own problems.
I only know 25 letters of the alphabet—I don’t know y.
I just don’t trust stairs, they’re always up to something.
I used to play piano by ear, but now I use my hands.
How do celebrities stay cool? They have many fans.
Why did the picture go to prison? Because it was framed.
How does a hurricane see? With one eye.
Where do polar bears keep their money? The snow bank.
What’s a tornado’s favorite game? Twister!
How does the moon cut his hair? Eclipse it.
What do you call a funny mountain? Hill-arious.
What gets wetter the more it dries? A towel.
What did the banana say to the boy? Nothing, bananas can’t talk!
What rock group has four men who don’t sing? Mount Rushmore.
My boss told me to have a good day, so I went home!
What do you call cheese that isn’t yours? Nacho cheese.
Did you get your haircut? No, I got them all cut.
I was wondering why the frisbee kept getting bigger and bigger. Then it hit me.
Wanna hear a joke about paper? Never mind. It’s tearable.
How many apples grow on a tree? All of them!
I talk to myself because sometimes I just need expert advice.
I used to be addicted to the hokey-pokey until I turned myself around.
What do you call someone who tells dad jokes but isn’t a dad? A faux pa.
I could tell a joke about pizza, but it’s a little cheesy.
If you see a crime at an Apple store, are you an iWitness?
I hate Velcro. It’s a rip off.
Spring is here! I got so excited that I wet my plants.
I had to sell my vacuum cleaner. All it was doing was gathering dust.
Do you know how many people are dead at a cemetery? All of them.
I’ll call you later. Don’t call me later, call me Dad.
If the early bird gets the worm, I’ll sleep in until there’s pancakes.
The wedding was so beautiful, even the cake was in tiers.
Why are spiders so smart? They can find everything on the web.
What do you call a toothless bear? A gummy bear!
What do you give a sick lemon? Lemon-aid.
What did the nose tell the finger? Stop picking on me!
Why can’t your hand be 12 inches long? Because then it would be a foot.
What kind of car does a sheep like to drive? A lamborghini.
What key is used to open bananas? A mon-key.
What has four wheels and flies? A garbage truck.
How do you talk to a giant? You use big words!
How do you make a tissue dance? Put a little boogie in it!
What kind of milk comes from a pampered cow? Spoiled milk.
What’s a sea monster’s favorite lunch? Fish and ships.
What do you call an alligator in a vest? An investigator.
Why are pigs so bad at sports? They always hog the ball.
Why shouldn’t you tell an egg a joke? It’ll crack up.
What’s a foot long and slippery? A slipper.
What’s a ninja’s favorite type of shoes? Sneakers!
What’s orange and sounds like a parrot? A carrot!
How does a penguin build a house? Igloos it together.
Why is no one friends with Dracula? He’s a pain in the neck.
Where do you learn all about ice cream? Sundae school.
Which bear is the most condescending? A pan-duh!
What kind of noise does a witch’s vehicle make? Brrrroooom, brrroooom.
What’s brown and sticky? A stick.
Two guys walked into a bar. The third guy ducked.
Did you hear about the actor who broke his leg onstage? He’s still in the cast.
How do you get a country girl’s attention? A tractor.
Why did the pharmacist walk on her tiptoes? She didn’t want to wake the sleeping pills.
I wanted to buy a pair of camouflage pants, but I couldn’t find any.
Why are elevator jokes so classic and good? They work on many levels.
I have an inferiority complex, but it’s not a very good one.
What do you call a pudgy psychic? A four-chin teller.
I had a date last night and it was perfect. Tomorrow, I’ll have a fig.
What did the police officer say to his belly-button? You’re under a vest.
What do you call it when a group of apes starts a company? Monkey business.
My wife asked me to stop singing Wonderwall to her. I said Maybe...
What kind of drink can be bitter and sweet? Reali-tea.
What do you call a naughty lamb dressed up like a skeleton for Halloween? Baaad to the bone.
Why did the lobster blush? Because it saw the ocean’s bottom!
Want to know why nurses like red crayons? Sometimes they have to draw blood.
What would the Terminator be called in his retirement? The Exterminator.
What did Tennessee? The same thing as Arkansas.
My wife asked me to go get 6 cans of Sprite from the grocery store. I realized when I got home that I had picked 7 up.
Why do bees have sticky hair? Because they use a honeycomb.
Why do some couples go to the gym? Because they want their relationship to work out.
What do you call an angry musician flipping someone off? A song bird.
Did you hear about the kidnapping at school? It’s fine, he woke up.
How can you tell it’s a dogwood tree? By the bark.
My boss told me to have a good day, so I went home.
Our vacuum cleaner is getting old. It’s just gathering dust.
Why did the man fall down the well? Because he couldn’t see that well.
Why is Peter Pan always flying? Because he Neverlands.
Which state has the most streets? Rhode Island.
What do you call 26 letters that went for a swim? Alphawetical.
What’s the name of a very polite, European body of water? Merci.
Why was the color green notoriously single? It was always so jaded.
I used to hate facial hair, but then it grew on me.
I want to make a brief joke, but it’s a little cheesy.
Why did the coach go to the bank? To get his quarter back.
How do celebrities stay cool? They have many fans.
Sundays are always a little sad, but the day before is a sadder day.
5/4 of people admit they’re bad at fractions.
Why did the bedding hide their relationship? They just wanted something pillow-key!
You’re American when you go into a bathroom and when you come out, but what are you while you’re in the bathroom? European.
I’ve been thinking about taking up meditation. I figure it’s better than sitting around doing nothing.
What did the flowers do when the bride walked down the aisle? They rose.
It takes guts to be an organ donor.
What do you get from a pampered cow? Spoiled milk.
What does Rockin’ Robin do when she’s bored? Tweet.
I lost my job at the bank on my first day. A woman asked me to check her balance, so I pushed her over.
Why did Waldo go to therapy? Because he needed to find himself.
How do you row a canoe filled with puppies? Bring out the doggy paddle.
Singing in the shower is fun until you get soap in your mouth. Then it becomes a soap opera.
Why were the utensils stuck together? They were spooning.
What’s a crafty dancer’s favorite hobby? Cutting a rug.
How does a penguin build his house? Igloos it together.
What kind of music do chiropractors like? Hip pop.
Where do you learn to make ice cream? At sundae school.
What kind of shoes does a lazy person wear? Loafers.
Why is cold water so insecure? Because it’s never called hot.
Justice is a dish best served cold. If it were served warm, it would be just-water.
I was going to tell a time-traveling joke, but you guys didn’t like it.
Shouldn’t the roof of your mouth actually be called the ceiling?
Why did the baby strawberry cry? Because its mother was in a jam.
Why couldn’t the toilet paper cross the road? Because it got stuck in a crack. %%Cross the road
Stop looking for the perfect match…use a lighter.
I told my doctor I heard buzzing, but he said it’s just a bug going around.
What kind of car does a sheep like to drive? A Lamborghini.
What do you call someone who won’t stick to a diet? A desserter.
What did the accountant say while auditing a document? This is taxing.
What did the two pieces of bread say on their wedding day? It was loaf at first sight.
If you see a burglary at an Apple store, you become an iWitness.
If the early bird gets the worm, I’ll sleep in until there’s pancakes.
Why do melons have weddings? Because they cantaloupe.
I signed up for a marathon, but how will I know if it’s the real deal or just a run through?
When you have a bladder infection, urine trouble.
What did the drummer call his twin daughters? Anna One, Anna Two!
What did the juicer say to the orange during self-quarantine? Can’t wait to squeeze you!
What do you call a toothless bear? A gummy bear!
Want to hear a joke about construction? I’m still working on it.
Someone told me that I should write a book. I said, That’s a novel concept.
Two goldfish are in a tank. One says to the other, Do you know how to drive this thing?
Why did the pony ask for a glass of water? Because it was a little horse.
What’s Forrest Gump’s password? 1forrest1
I tell dad jokes, but I don’t have any kids. I’m a faux pa.
What does a nosey pepper do? It gets jalapeño business.
How can you mend a broken pumpkin? Use a pumpkin patch.
If a child refuses to nap, are they guilty of resisting a rest?
Why do dads feel the need to tell such bad jokes? They just want to help you become a groan up.
I know a lot of jokes about retired people, but none of them work.
Why are spiders so smart? They can find everything on the web.
What do you call spiders who just got married? Newly-webs.
RIP boiled water—you will be mist.
What do you call two octopuses that look the same? Itenticle.
What has one head, one foot, and four legs? A bed.
Sore throats are a pain in the neck.
What does a house wear? Address.
Why did the scarecrow win an award? He was out standing in his field.
What is a scarecrow’s favorite fruit? Straw-berries.
What’s red and smells like blue paint? Red paint.
My son asked me to put his shoes on, but I don’t think they’ll fit me.
I’ve been bored recently, so I decided to take up fencing. The neighbors keep demanding that I put it back.
How do you know when a chicken is evil? It lays deviled eggs.
What do you call an unpredictable camera? A loose Canon.
I didn’t get a haircut, I got them all cut.
Which U.S. state is known for its especially small soft drinks? Minnesota.
What do sprinters eat before a race? Nothing—they fast.
What did one Dorito farmer say to the other? Cool Ranch!
How do cows shop? From cattle-logs.
I’m so good at sleeping, I can do it with my eyes closed.
People are usually shocked that I have a Police record. But I love their greatest hits!
I told my girlfriend she drew on her eyebrows too high. She seemed surprised.
What do you call a fibbing cat? A lion.
Why shouldn’t you write with a broken pencil? Because it’s pointless.
I like telling Dad jokes…sometimes he laughs.
How do you weigh a millennial? In Instagrams.
The wedding was so beautiful, even the cake was in tiers.
What’s the most patriotic sport? Flag football.
Why were spectators confused by the koala’s self-portrait? It was bear.
Why did the envelope take so long to get ready? It had to get addressed.
What does a karate master get rewarded with while driving? A seat belt.
What do you call a baby sheep that knows karate? A lamb chop.
What did the husband say to his wife right after getting LASIK surgery? Aren’t you a sight for sore eyes?
Why are pigs bad drivers? Because they hog the road.
What do lions use to look at their manes? Mirroars.
What did the dad say when his golden retriever was caught eating a hot dog? It’s a dog eat dog world out there.
Do mascara and lipstick ever argue? Sure, but then they makeup.
What piece on the playground is always exhausted? The tire swing.
Why did two tall people get along so well? They could really see eye to eye.
Why was the gossip disliked at the coffee shop? She always spilled the tea.
What does a writer have in common with a football player? Anxiety over a rough draft.
Where do wasps like to get lunch? A bee-stro.
Is there anything worse than when it’s raining cats and dogs? Yes! Hailing taxis.
Why would doors do well on social media? Everyone looks for their handles.
Why did the physicist and the biologist break up? Because they had no chemistry.
If you feel like someone is watching you, you’re not alone.
Which bathroom appliance would be the worst life preserver? The sink.
Why was the dad sitting on a pack of playing cards? His kid asked him to sit on the deck.
How do birds learn how to fly? They wing it!
What kind of bird is always getting hurt? The owl.
What’s either a really gross animal issue OR an impressive, magical school? Hogwarts.
How does Darth Vader like his toast? On the dark side.
What did the dishwasher say to the oven after a productive day? You’ve been on fire!
Why did the tomato blush? Because it saw the salad dressing.
Why did the cashier rip money in half? They were asked to break a bill.
What did one furniture maker say to another during a tense discussion? Let’s table this.
I was going to tell a joke about water, but it was too tasteless.
Why couldn’t the duck be quiet? Because it was addicted to quack.
Why was the ghost so tired? He worked the graveyard shift. %%Halloween
Why do pancakes always win at baseball? They have the best batter.
Why did the baseball player get arrested? Because he stole second base.
Why couldn’t the couple get married at the library? It was all booked up.
Why did the pug buy a clock? It wanted to be a watchdog.
Where do hamburgers go to dance? The meatball.
How did the dad prank his daughter using fake dog poop on April Fools Day? He told her to look out for her new sham-poo in the shower.
What did the air conditioner say when it met a celebrity? I’m a big fan.
What was Sherlock Holmes’ favorite protein source? Mystery meat.
What did the dryer say to the boring duvet cover that just got out of the washer? Don’t be such a wet blanket.
Why couldn’t the bike stand up on its own? Because it was too tired.
Why was the cow such a heartthrob on the farm? He was a s-moo-th talker.
What’s a writer’s favorite train station? Penn Station.
What do you call a gnat with a sore throat? A hoarse fly.
What was said about the messy, angry man who was eating a can of Pringles? He’s got a chip on his shoulder.
What’s it called when kittens get stuck in a tree? A cat-astrophe.
What kind of shape may have been knighted? Sir-cles.
Why is sand so optimistic? It has a can-dune attitude.
What has four wheels and flies? A garbage truck.
What part of the museum makes everyone sneeze? The sta-tues.
What did the baker say when she won an award? It was a piece of cake.
Why couldn’t the couple respond right away when looking at wedding venues? They were engaged.
What is Marco’s favorite clothing store? Polo.
What do you call it when a lawyer takes a test early in the morning? A breakfast bar.
What do frogs use to track their exercise? Fit (rib)bits.
How do frogs invest their money? They use a stock croaker.
Why did police arrest the turkey? They suspected fowl play.
What kind of cleaning product feels a lot of motivation in life? All-purpose.
Where was the dripping coming from in the fridge? The leeks.
Why was the hockey player gifted a new cap? He was known for his hat tricks.
What vegetable is kind to everyone? The sweet potato.
How was the handsome runner described? Dashing.
What animals are the best to call if you get locked out of your house? Monkeys.
What did the geometry teacher say when the class had trouble solving a problem? Let’s try a different angle.
Why don’t phones ever go hungry? They have plenty of apps to choose from.
Why couldn’t the family leave the room after playing with Legos? They were blocked.
What makes a basketball court trendy and accessorized? The hoops.
What did the sapphire’s best friend tell her? You’re a real gem.
Getting paid to sleep is a true dream job.
Did you hear about the bossy man at the bar? He ordered everyone around.
What do you give the dentist of the year? A little plaque.
Why did the deer go to the dentist? It had buck teeth.
Why did the Oreo go to the dentist? Because it lost its filling.
What happens when doctors get frustrated? They lose their patients.
Why was the traffic light late to work? It took too long to change.
Did you hear about the guy who was afraid of hurdles? He got over it.
Why didn’t the sun go to college? It already had a million degrees.
Did you hear about the guy who drank invisible ink? He’s at the hospital waiting to be seen.
What do you call a can opener that doesn’t work? A can’t opener.
What do lawyers wear to work? Law suits.
I used to be a banker, but I lost interest.
Why did the computer catch cold? It left a window open.
What do computers eat for a snack? Microchips.
Why did the computer go to bed? It needed to crash.
Why did the employee get fired from the keyboard factory? He wasn’t putting in enough shifts.
How do trees get on the internet? They log in.
Why did the computer get glasses? To improve its website.
What kind of bird works on a construction site? A crane.
How much money does a skunk have? Only one scent.
Why did the watch go on vacation? Because it needed to unwind.
What does a painter do when he gets cold? Puts on another coat.
How do you tell a scientist that they have bad breath? Offer them an experi-mint.
How did the barber win the race? He knew a shortcut.
Why did the roofer go to the doctor? He had shingles.
Dogs can’t operate MRI machines, but cats-can.
What does a librarian use to go fishing? A bookworm.
What did the roof say to the shingle? The first one is on the house.
Why did the tailor get fired? He wasn’t a good fit.
What kind of bug can tell time? A clock-roach.
Why did the girl toss a clock out the window? She wanted to see time fly.
When does Friday come before Thursday? In the dictionary.
How many telemarketers does it take to change a light bulb? Only one, but he has to do it while you are eating dinner.
How many narcissists does it take to screw in a light bulb? One. The narcissist holds the light bulb while the rest of the world revolves around him.
How many DIY buffs does it take to change a light bulb? One, but it takes two weeks and four trips to the hardware store.
How many paranoids does it take to change a light bulb? Who wants to know?
I read that by law you must turn on your headlights when it’s raining in Sweden, but how am I supposed to know when it’s raining in Sweden?
I was addicted to the hokey pokey…but I turned myself around.
I don’t trust stairs. They are always up to something.
Today, my son asked, Can I have a bookmark? I burst into tears—11 years old and he still doesn’t know my name is Brian.
When I was a kid, my dad got fired from his job as a road worker for theft. I refused to believe he could do such a thing, but when I got home, the signs were all there.
Why didn’t Han Solo enjoy his steak dinner? It was Chewie.
Why don’t pirates take a bath before they walk the plank? They just wash up on shore.
Why do you never see elephants hiding in trees? Because they’re so good at it.
Did you hear about the racing snail who got rid of his shell? He thought it would make him faster, but it just made him sluggish.
A turtle is crossing the road when he’s mugged by two snails. When the police ask him what happened, the shaken turtle replies, I don’t know. It all happened so fast.
Did you hear about the guy who froze to death at the drive-in? He went to see Closed for the Winter.
We all know about Murphy’s Law: Anything that can go wrong will go wrong. But have you heard of Cole’s Law? It’s thinly sliced cabbage.
When does a joke become a dad joke? When it becomes apparent.
I had a happy childhood. My dad used to put me in tires and roll me down hills. Those were Goodyears.
What invention allows us to see through walls? Windows.
I know a bunch of good jokes about umbrellas, but they usually go over people’s heads.
The bank keeps calling me to give me compliments. They say I have an outstanding balance.
What is the most popular fish in the ocean? A starfish.
Barbers…you have to take your hat off to them.
What did one plate say to another plate? Tonight, dinner’s on me.
Did you hear about the surgeon who enjoyed performing quick surgeries on insects? He did one on the fly.
What’s a vampire’s favorite ship? A blood vessel. %%Halloween
There’s only one thing I can’t deal with, and that’s a deck of cards glued together.
The past, the present, and the future walked into a bar. It was tense.
Son: Dad, I’m hungry. Dad: Hi hungry, I’m Dad.
Dad: Did you hear about the kidnapping at school? Son: No. What happened? Dad: The teacher woke him up.
Daughter: I have a lot of friends named Nathan. There’s Nathan Miller, Nathan Radcliff, Nathan Lewis… Me: When they are together, do you call them the United Nathans?
What’s the least-spoken language in the world? Sign language.
What do you call a hippie’s wife? Mississippi.
I searched for a lighter on Amazon, but all I could find were 6,000 matches.
I sold our vacuum cleaner; it was just gathering dust.
What did the evil chicken lay? Deviled eggs.
Did you hear they arrested the devil? Yeah, they got him on possession.
A friend of mine didn’t pay his exorcist. He got repossessed.
How do you make holy water? You boil the hell out of it.
What sound does a witch’s car make? Broom broom! %%Halloween
I want to go on record that I support farming. As a matter of fact, you could call me protractor.
What’s the best way to watch a fly-fishing tournament? Live stream.
How do you tell the difference between an alligator and a crocodile? You will see one later and one in a while.
Did you hear about the crustacean accused of promoting his own shellfish interests?
Did you hear about the bankrupt poet who ode everyone?
Did you hear about the shepherd who drove his sheep through town and was given a ticket for making a ewe turn?
Did you hear about the cat who ate a ball of yarn? She had mittens.
Did you hear about the claustrophobic astronaut? He just wanted a little more space.
Why did the man name his dogs Rolex and Timex? Because they were watchdogs.
What do you call a dog that can do magic? A Labracabrador.
Why do dogs float in water? Because they are good buoys.
What happens when it rains cats and dogs? You have to be careful not to step in a poodle.
What do you call 50 pigs and 50 deer? 100 sows and bucks.
Why do cows wear bells? Because their horns don’t work.
What do you call a fish with no eye? A fsh.
Police arrested a bottle of water because it was wanted in three different states: solid, liquid, and gas.
What do you call a lazy kangaroo? Pouch potato.
Why is grass so dangerous? Because it’s full of blades.
What is the Easter bunny’s favorite type of music? Hip-hop.
A friend of mine is known for sweeping girls off their feet. He’s an extremely aggressive janitor.
I’m an expert at picking leaves and heating them in water. It’s my special tea.
My son’s fourth birthday was today. When he came to see me, I didn’t recognize him at first. I had never seen him be four.
I recently went to the World’s Tiniest Wind Turbine exhibit. Honestly, not a big fan.
I was out on a walk when I saw a sign that said, Man wanted for robbery. So I went in and applied for the job.
How long should socks be? Twelve inches, so you can fit in one foot.
Did you hear the joke about experiencing déjà vu? Did you hear the joke about experiencing déjà vu?
A bartender broke up with her boyfriend, but he kept asking her for another shot.
I’m reading a novel where the main character has strained the muscles around his spine. That’s his back story.
My doctor told me I’ve really grown as a person. Well, her exact words were that I gained excess weight.
What do you call someone who always states the obvious? Someone who always states the obvious.
Scientists have discovered what is believed to be the world’s largest bedsheet. More on this story as it unfolds.
3.14 percent of sailors are pi-rates.
You can’t plant flowers if you haven’t botany.
What did the French chef give his wife for Valentine’s Day? A hug and a quiche.
A ham sandwich walks into a bar and orders a beer. The bartender says, Sorry, we don’t serve food here.
A couple of cups of yogurt walk into a country club. We don’t serve your kind here, the bartender says. Why not? one yogurt asks. We’re cultured.
A brain walks into a bar and takes a seat. I’d like some wings and a pint of beer, please, it says. Sorry, but I can’t serve you, the bartender replies. You’re out of your head.
A pirate walks into a bar with a paper towel on his head. The bartender says, What’s with the paper towel? The pirate says, Arrr! I’ve got a Bounty on me head!
A guy walks into a bar, and there’s a horse serving drinks. The horse asks, What are you staring at? Haven’t you ever seen a horse tending bar before? The guy says, It’s not that. I just never thought the parrot would sell the place.
Why did Beethoven get rid of his chickens? All they said was, Bach, Bach, Bach…
What did one DNA say to the other DNA? Do these genes make me look fat?
What do youneed to make a small fortune on Wall Street? A large fortune.
How does the man in the moon get his hair cut? Eclipse it.
Did you hear about the restaurant on the moon? Great food, no atmosphere.
Did you hear the one about the kid who started a business tying shoelaces on the playground? It was a knot-for-profit.
My kid wants to invent a pencil with an eraser on each end, but I just don’t see the point.
Teacher: There are two words I don’t allow in my class. One is gross, and the other is cool. Johnny: So, what are the words?
Why should you never mention the number 288? It’s two gross
I spent a lot of time, money, and effort childproofing my house, but the kids still get in.
A cheese factory exploded in France. Da brie is everywhere!
Did you hear the rumor about butter? Well, I’m not going to spread it!
Why do melons have weddings? Because they cantaloupe.
What do Bostonians call a fake noodle? An impasta.
A college education now costs $100,000, but it produces three very proud people: the student, his mama, and his pauper.
My son has his BA and his MA, but his P­A still supports him.
What does a mobster buried in cement soon become? A hardened criminal.
What does idk stand for? Everyone I ask says, I don’t know.
Why was the pig covered in ink? Because it lived in a pen.
Did you hear about the guy who stole 50 cartons of hand sanitizer? They couldn’t prosecute—his hands were clean.
Why was the rookie police officer assigned to hunt the cannibal? The more seasoned officers had already been eaten.
What do you call a snitching scientist? A lab rat.
What’s the difference between a man wearing pajamas on a bicycle and a guy wearing a tuxedo on a unicycle? Attire.
It’s a shame that the Beatles didn’t make the submarine in that song green. That would’ve been sublime.
Did you hear about the aquatic sea mammals that escaped from the zoo? It was otter chaos.
What did the skeleton order with its beer? A mop.
Why do nurses like red crayons? Sometimes they have to draw blood.
How much do I love crunchy tacos? From my head tomatoes. %%Cinco De Mayo
What kind of spells do leprechauns use? Lucky Charms.
What do you call a bear with no teeth? A gummy bear.
My IQ test results came back. They were negative.
What do you get when you cross a polar bear with a seal? A polar bear.
Did you hear about the nurse who was chewed out by the doctor because she was absent without gauze?
If athletes get athlete’s foot, what do astronauts get? Missile toe.
My wife asked me to sync her phone, so I threw it into the ocean.
My wife is really mad that I have no sense of direction. I packed up my stuff and right.
What did one cannibal say to the other while they were eating a clown? Does this taste funny to you?
Do I enjoy making courthouse puns? Guilty.
What do you call someone with no body and no nose? Nobody knows.
You know, people say they pick their nose, but I feel like I was just born with mine.
In a freak accident today, a photographer was killed when a huge lump of cheddar landed on him. To be fair, the people who were being photographed did try to warn him.
Can February March? No, but April May.
Not sure if you have noticed, but I love bad puns. That’s just how eye roll.
If you see a robbery at an Apple store, does that make you an iWitness?
What did the drummer call his twin daughters? Anna one, Anna two…
What’s a bad wizard’s favorite computer program? Spell check.
I was just reminiscing about the beautiful herb garden I had when I was growing up. Good thymes.
I began to read a horror novel in braille. Something bad is about to happen—I can feel it.
Why do pumpkins sit on porches? They have no hands to knock on the door.
My friend wants to become an archaeologist, but I’m trying to put him off. I’m convinced his life will be in ruins.
I got hit in the head with a can of Coke today. Don’t worry, I’m not hurt. It was a soft drink.
Cooking out this weekend? Don’t forget the pickle. It’s kind of a big dill.
Justice is a dish best served cold. If it were served warm, it would be justwater.
What’s orange and sounds like a parrot? A carrot.
A steak pun is a rare medium done well.
Why did the raisin go out with the prune? Because he couldn’t find a date.
What’s brown and sticky? A stick.
My dog accidentally swallowed a bunch of Scrabble tiles. I think this could spell disaster.
I wondered why the ball was getting bigger. Then it hit me.
I had a date last night. It was perfect. Tomorrow, I’ll try a grape.
Armed robbers—some say they’re a drain on society, but you’ve got to give it to them.
It hurts me to say this, but I have a sore throat.
I know a surgeon who puts organs back in upside down. I told him that’s not funny, but he said it was an inside joke.
My girlfriend says it’s either her or my career as a news reporter. I have some breaking news for her.
Inflation is really getting out of hand, but that’s just my five cents.
I can guess what people do for a living just by looking at their hands. I mean, I’m usually wrong, but I can guess.
I’ve been breeding racing deer. Just trying to make a quick buck.
How many mystery writers does it take to change a light bulb? Two: One to screw it in most of the way and another to give it a surprise twist at the end.
My dentist offered me dentures for only a dollar. It sounded like a good deal at the time, but now I have buck teeth.
"""

def parse_joke_line(line, joke_id):
    line = line.strip()
    if not line:
        return None

    # Replace curly apostrophes with straight ones FIRST
    text_to_process = line.replace("\u2019", "'").replace("’", "'")

    parts = text_to_process.split('%%', 1)
    # Process text part first (which now has straight apostrophes)
    text = parts[0].strip().replace('\"', '"') # Handle escaped quotes if any (though unlikely with straight apostrophes)

    categories = []
    if len(parts) > 1 and parts[1].strip():
        raw_categories = parts[1].strip()
        potential_categories = re.split(r'[\s,]+', raw_categories)
        for cat in potential_categories:
            cat_cleaned = cat.strip()
            if cat_cleaned: 
                categories.append(cat_cleaned)
    
    # Fallback for single '%' only if no categories found yet and '%%' was not in the original line
    if not categories and '%' in parts[0] and '%%' not in text_to_process : # Check against text_to_process
        # Reprocess parts[0] because it might contain the single '%'
        # and ensure it also has apostrophes straightened
        parts_single_percent_text = parts[0].replace("\u2019", "'").replace("’", "'")
        parts_single_percent = parts_single_percent_text.split('%', 1)
        text = parts_single_percent[0].strip().replace('\"', '"') # Update text if it was re-split
        
        if len(parts_single_percent) > 1 and parts_single_percent[1].strip():
            raw_categories_single = parts_single_percent[1].strip()
            potential_categories_single = re.split(r'[\s,]+', raw_categories_single)
            for cat_s in potential_categories_single:
                cat_s_cleaned = cat_s.strip()
                if cat_s_cleaned:
                    categories.append(cat_s_cleaned)

    return {
        "id": joke_id,
        "text": text, 
        "categories": sorted(list(set(c.capitalize() for c in categories if c))) 
    }

jokes = []
joke_id_counter = 1

# Process the multiline JOKE_DATA
for line in JOKE_DATA.strip().split('\n'):
    if len(line.strip()) < 3: 
        continue
    
    # No need to process apostrophes here if parse_joke_line handles it for the whole line input
    # processed_line = line.replace("\u2019", "'").replace("’", "'") # This was redundant

    joke_data = parse_joke_line(line, joke_id_counter) # Pass original line, parse_joke_line does apostrophe replacement
    if joke_data and joke_data['text']: 
        jokes.append(joke_data)
        joke_id_counter += 1

# Write to jokes.json
try:
    with open('jokes.json', 'w', encoding='utf-8') as f:
        json.dump(jokes, f, indent=4, ensure_ascii=False) 
    print(f"Successfully created jokes.json with {len(jokes)} jokes, using straight apostrophes.")
except Exception as e:
    print(f"Error writing jokes.json: {e}")
    try:
        with open('jokes.json', 'w', encoding='utf-8') as f:
            json.dump([], f, indent=4, ensure_ascii=False)
        print("Wrote an empty list to jokes.json due to the error.")
    except Exception as e_fallback:
        print(f"Fallback write to jokes.json also failed: {e_fallback}")
