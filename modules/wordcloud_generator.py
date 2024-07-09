import pandas as pd
from wordcloud import WordCloud
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
from collections import Counter
import matplotlib.pyplot as plt

# Download necessary NLTK data
nltk.download('punkt')

def load_stopwords(file_path):
    """Load stopwords from a CSV file."""
    df = pd.read_csv(file_path)
    stopwords_list = df[df.columns[0]].tolist()
    return set(stopwords_list)

def preprocess_text(text, stopwords_set):
    """Preprocess text by removing non-alphanumeric characters and stopwords."""
    text = re.sub(r'[^A-Za-z\s]', '', text)  # Remove non-alphanumeric characters
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens]
    tokens = [word for word in tokens if word.isalnum() and word not in stopwords_set]
    return tokens

def generate_word_cloud_from_text(text, stopwords_set, output_path):
    """Generate a word cloud image from a single text string."""
    preprocessed_tokens = preprocess_text(text, stopwords_set)
    word_frequencies = Counter(preprocessed_tokens)
    
    wordcloud = WordCloud(
        width=1600,
        height=800,
        background_color='white',
        collocations=False,
        max_words=200,
        contour_width=3,
        contour_color='steelblue',
        prefer_horizontal=1.0,
        max_font_size=300,
        min_font_size=20,
        scale=5,
    )
    wordcloud.generate_from_frequencies(word_frequencies)
    
    plt.figure(figsize=(16, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(output_path, format="png", dpi=1000, bbox_inches='tight')
    plt.close()
    
def update_dataset_and_generate_word_cloud(input_string, dataset_path, stopwords_set, output_path):
    """Update dataset with a new text string and generate a word cloud image."""
    # Read the existing dataset
    dataset = pd.read_csv(dataset_path)
    
    # Preprocess and add the new string to the dataset
    preprocessed_tokens = preprocess_text(input_string, stopwords_set)
    new_row = pd.DataFrame({'clean_text': [' '.join(preprocessed_tokens)]})
    dataset = pd.concat([dataset, new_row], ignore_index=True)
    
    # Save the updated DataFrame to the CSV file
    dataset.to_csv(dataset_path, index=False)
    
    # Compute word frequencies from the updated dataset
    word_frequencies = Counter()
    for text in dataset['clean_text'].dropna():
        tokens = preprocess_text(text, stopwords_set)
        word_frequencies.update(tokens)
    
    # Generate and save the word cloud image
    wordcloud = WordCloud(
        width=1600,
        height=800,
        background_color='white',
        collocations=False,
        max_words=200,
        contour_width=3,
        contour_color='steelblue',
        prefer_horizontal=1.0,
        max_font_size=300,
        min_font_size=20,
        scale=5,
    )
    wordcloud.generate_from_frequencies(word_frequencies)
    
    plt.figure(figsize=(16, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(output_path, format="png", dpi=1000, bbox_inches='tight')
    plt.close()


# Test the methods
stopwords_file_path = 'Datasets/stopwords_english.csv'
dataset_path = 'Datasets/legal_merged_dataset.csv'
output_path_single = 'wordcloud_single.png'
output_path_dataset = 'wordcloud_dataset.png'
input_string = """
Edison High School
Athletic Contract
1. To be eligible for any team, the student must meet CIF, SUSD and Edison High School eligibility
requirements. SUSD and the State of California require a Grade Point Average (GPA) of 2.00 and the
student athlete must maintain credits towards graduation. Eligibility will be checked each semester.
2. All athletes must pass a physical examination and have it uploaded into FamilyID. The athlete and
parents must sign the emergency information and the player packet signature form. This form needs to be
submitted to FamillyID before the student is allowed to compete.
3. An athlete may change from one sport to another only if he/she has permission from both coaches. An
athlete is not allowed to quit a sport from one season to go out for another sport the next season. The
athlete MUST finish the sport from the previous season.
4. An athlete MUST be in school a minimum of 2 classes in order to participate in a game or practice held
on that day. A legal admit must be presented if the athlete misses any part of school on a game or
practice day in order to be considered for participation.
5. An athlete MUST attend practices in order to play in the games. It is up to the coach and the individual
sports program to determine the discipline for missed practices (see program guidelines)
6. A student athlete will immediately become ineligible and could lose all playing privileges for that season
of sport for any of the following reasons:
A. Quitting a sport without a justifiable reason or consent of the coach.
B. Smoking, drinking, and/or the use of illegal drugs.
C. Acting in a manner that may bring dishonor or shame to the community or school.
D. Fighting or coming off the bench or sideline during any fight on the playing area.
E. Consistent discipline, academic and/or attendance issues.
F. Participation in a non-school sponsored team, such as city league, shall make the athlete ineligible for
a school team of that same sport if the participation is during the season.
**Eligibility may be earned back at the discretion of administration and / or the coach
7. Student-Athletes are representatives of EHS and at all times must conduct themselves in a manner
that reflects positively on their teams, school and community
Failure to comply with any of the requirements stated in this contract will be referred to the
Coach, the Director of Athletics and/or the Administration for appropriate discipline outlined in
our code violations.
Code Violations and Team Disciplinary Action:
1. Smoking/Distribution/Sale or Use of Tobacco Products - First Violation: Ten (10) day suspension
from all scrimmages and contests . A suspended player is required to participate in all practices. Second
Violation: Twenty (20) day suspension from all scrimmages and contests. Third Violation: Will result in
forfeiture of eligibility to participate in athletics for one (1) year from the point of infraction.
2. Smoking/Distribution/Sale or Use of Marijuana or Marijuana Products - First Violation: Ten (10) day
suspension from all scrimmages and contests . A suspended player is required to participate in all
practices. Second Violation: Twenty (20) day suspension from all scrimmages and contests. Third
Violation: Will result in forfeiture of eligibility to participate in athletics for one (1) year from the point of
infraction.
3. Possession of and/or Consumption of Alcohol and Over the Counter Performance Enhancing
Products. First Violation: Ten (10) day suspension from all scrimmages and contests. A suspended player
is required to participate in all practices. Second Violation: Twenty (20) day suspension from all
scrimmages and contests. Third Violation: Will result in forfeiture of eligibility to participate in athletics for
one (1) year from the point of infraction.
4. Fighting- 45 day social probation(suspension interventions document)
5. Theft or Vandalism: to any school property (Home or Away) while under the supervision of a coach
or while representing the school team in any way. First Violation: Ten (10) day suspension from all
scrimmages and contests. A suspended player is required to participate in all practices. Second Violation:
Twenty (20) day suspension from all scrimmages and contests. Third Violation: Will result in forfeiture of
eligibility to participate in athletics for one (1) year from the point of infraction.
6. Conduct Unbecoming or Other Actions or Excessive Misbehavior: that would reflect negatively
upon the team or school. First Violation: Ten (10) day suspension from all scrimmages and contests. A
suspended player is required to participate in all practices. Second Violation: Twenty (20) day suspension
from all scrimmages and contests. Third Violation: Will result in forfeiture of eligibility to participate in
athletics for one (1) year from the point of infraction.(ex. Running to/instigating/recording or being present
at a fight)
7. Cutting Class: If a student is found cutting a class more than once in a day, that student will be
suspended from all activity that same day. That includes practices, as well as scrimmages, games, meets
and matches. If the multiple cuts goes undetected until the next school day, then the suspension will take
effect immediately for that school day
*NOTE: Suspensions will be carried over to the next season of participation
I,(print name)___________________________, have read, understand, and agree to follow the Edison
High school Athletic Contract
_______________________________________ __________________
Student Signature Date
_______________________________________ __________________
Parent Signature Date

"""

# Load stopwords
stopwords_set = load_stopwords(stopwords_file_path)

# Generate word cloud from a single text string
generate_word_cloud_from_text(input_string, stopwords_set, output_path_single)

# Update dataset and generate word cloud
update_dataset_and_generate_word_cloud(input_string, dataset_path, stopwords_set, output_path_dataset)
