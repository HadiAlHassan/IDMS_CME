import PyPDF2
from pathlib import Path
import spacy
from langdetect import detect
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import re
import json

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_metadata_pdf(file_path):
    # Read PDF
    with open(file_path, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        text = ""
        metadata = pdf_reader.metadata
        
        for page in pdf_reader.pages:
            text += page.extract_text()

    document_metadata = {
        'title': metadata.get('/Title', 'No title found'),
        'author': metadata.get('/Author', 'No author found'),
        'summary': summarize_text(text),
        'language': detect_language(text),
        'confidentiality': extract_confidentiality(text),
        'locations': extract_locations(text),
        'references': extract_references(text),
        'in_text_citations': extract_in_text_citations(text),
        'word_count': count_words(text)
    }

    return document_metadata

def summarize_text(text, num_sentences=5):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return " ".join([str(sentence) for sentence in summary])

def detect_language(text):
    return detect(text)

def extract_confidentiality(text):
    # Simple regex-based search for confidentiality terms
    confidentiality_terms = ['confidential', 'proprietary', 'sensitive', 'classified']
    for term in confidentiality_terms:
        if re.search(r'\b' + term + r'\b', text, re.IGNORECASE):
            return True
    return False

def extract_locations(text):
    doc = nlp(text)
    locations = set()
    for ent in doc.ents:
        if ent.label_ == 'GPE':  # GPE = Geopolitical Entity
            locations.add(ent.text)
    return list(locations)

def extract_references(text):
    # Simple regex-based search for references (e.g., URLs, DOIs)
    urls = re.findall(r'(https?://\S+)', text)
    dois = re.findall(r'\b10.\d{4,9}/[-._;()/:A-Z0-9]+\b', text, re.IGNORECASE)
    return {'urls': urls, 'dois': dois}

def extract_in_text_citations(text):
    # Regex to find in-text citations like (Author, Year) or [Number]
    author_year_citations = re.findall(r'\(([^)]+, \d{4})\)', text)
    number_citations = re.findall(r'\[\d+\]', text)
    return {'author_year': author_year_citations, 'number': number_citations}

def count_words(text):
    words = text.split()
    return len(words)

# Example usage
file_name = "Best-Cases-19-7.26.pdf"
file_path = Path("C:/Users/LuidovicZgheib.INTERN27-PC/Desktop/Project_Clone/pdfs") / file_name

# Ensure the full path is used
print(file_path.resolve())

metadata = extract_metadata_pdf(file_path)

# Store the metadata in a JSON file
output_path = Path("C:/Users/LuidovicZgheib.INTERN27-PC/Desktop/Project_Clone/pdfs") / "metadata.json"
with open(output_path, 'w', encoding='utf-8') as json_file:
    json.dump(metadata, json_file, indent=4)

print(f"Metadata has been saved to {output_path}")

#####################################################################################################################

import spacy
from langdetect import detect
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import re
import json

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_metadata_text(text):
    # Extract title using regex
    title_match = re.search(r'([^\n\r]+)', text.strip())
    title = title_match.group(0).strip() if title_match else 'No title found'

    # Extract author using regex
    author_match = re.search(r'Author: ([^\n\r]+)', text)
    author = author_match.group(1).strip() if author_match else 'No author found'

    document_metadata = {
        'title': title,
        'author': author,
        'summary': summarize_text(text),
        'language': detect_language(text),
        'confidentiality': extract_confidentiality(text),
        'locations': extract_locations(text),
        'references': extract_references(text),
        'in_text_citations': extract_in_text_citations(text),
        'word_count': count_words(text)
    }

    return document_metadata

def summarize_text(text, num_sentences=5):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return " ".join([str(sentence) for sentence in summary])

def detect_language(text):
    return detect(text)

def extract_confidentiality(text):
    # Simple regex-based search for confidentiality terms
    confidentiality_terms = ['confidential', 'proprietary', 'sensitive', 'classified']
    for term in confidentiality_terms:
        if re.search(r'\b' + term + r'\b', text, re.IGNORECASE):
            return True
    return False

def extract_locations(text):
    doc = nlp(text)
    locations = set()
    for ent in doc.ents:
        if ent.label_ == 'GPE':  # GPE = Geopolitical Entity
            locations.add(ent.text)
    return list(locations)

def extract_references(text):
    # Simple regex-based search for references (e.g., URLs, DOIs)
    urls = re.findall(r'(https?://\S+)', text)
    dois = re.findall(r'\b10.\d{4,9}/[-._;()/:A-Z0-9]+\b', text, re.IGNORECASE)
    return {'urls': urls, 'dois': dois}

def extract_in_text_citations(text):
    # Regex to find in-text citations like (Author, Year) or [Number]
    author_year_citations = re.findall(r'\(([^)]+, \d{4})\)', text)
    number_citations = re.findall(r'\[\d+\]', text)
    return {'author_year': author_year_citations, 'number': number_citations}

def count_words(text):
    words = text.split()
    return len(words)

# Example usage with text string
sample_text = """
Best of Case Law – Reading materials
Contents
Class 1: The Purpose of the Corporation (Dodge v. Ford Motor Company)........................ 1
James Fallows, How the World Works, The Atlantic (December 1993)............................ 2
Dodge v. Ford Motor Co., 170 N.W. 668 (Mich. 1919)...................................................... 10
Class 2: Shareholders versus Directors (Blasius Industries, Inc. v. Atlas Corp.)............... 15
Blasius Industries, Inc. v. Atlas Corp., 564 A.2d 651(Del. 1988).................................... 17
Class 1: The Purpose of the Corporation (Dodge v. Ford Motor Company)
Dodge v. Ford Motor Company is a great case. It is important because its ruling touches on a 
question at the very core of corporate law: what is the purpose of the corporation? Is it exclusively 
to make the most money for shareholders? (And if so – making the most money long-term or shortterm?) Or perhaps it is also permissible – or even required – that the corporation would act in the 
interests of other stakeholders – employees, creditors, customers, the local community, or the 
nation in which it is incorporated?
But there is another reason why Dodge v. Ford Motor Company is a great case: the parties are 
pretending to act for reasons different than those that really motivate them. As we will see in class, 
the plaintiff and defendant present their interests in ways that don’t make sense once you think 
things through. And read narrowly, the court’s decision seems almost arbitrary and in contrast to 
established law. But once you understand the entire context, the court ruling can be seen as a 
clever way to maintain both the letter and the spirit of established law.
But no case is perfect. The main weakness of Dodge is that it is not well-written; indeed, it is quite 
boring to read. Another weakness is that the actual legal question it discusses is a narrow one that 
requires knowing some corporate law to understand. Therefore, though I am including the text of 
the case for you to read ahead of class, it is not the main assignment and you should not feel 
frustrated if it’s not clear to you. I will explain the case in class.
Rather, the main reading assignment ahead of class is an excerpt from an old magazine article, 
about an economist you may never have heard about – Friedrich List. I think this is a more 
enjoyable reading, and it will give you background for a discussion on the big policy question 
Dodge tackles: whose interests should the corporation serve?
No doubt you have heard of Adam Smith and later classical economists who espoused free-market 
economics, based on the idea that self-interested behavior by market participants enriches society 
as a whole. The line of corporate law doctrine that fits with this worldview is the norm that a 
corporation should operate solely for the purpose of its shareholders, and that this would ultimately 
benefit all other stakeholders (employees, customers, society as a whole, etc.).
Friedrich List is a leading intellectual force behind an opposing view, which is why I ask that you 
read the article to understand the main differences between his world view and that of his freemarket opponents (which he called the “cosmopolitans”). While List is not widely known today, 
his work is credited with influencing the thinking of several policy makers and leaders, including 
China’s Deng Xiaoping.
In some ways, List appears more relevant to political debate today – with the rise of populist 
politicians in several countries including the U.S. – than it was when the article was written. But 
in other ways, this article is very much a product of its time. To a contemporary reader it may 
appear odd how much Japan and Germany are mentioned in the article compared to other countries 
(for example, China). But this was very typical of American policy analysis (and popular culture) 
in the 1980s. At that time, the American economy was relatively stagnant, while the economies 
of Japan and Germany were booming. The US had a large trade deficit with these countries, with 
cheaper German and Japanese imports crowding out a shrinking American industry, and German 
and Japanese firms used the dollars they acquired from the deficit to acquire iconic American 
assets. The result was fear of those two countries on one hand, and a desire to mimic them on the 
other hand. The article is in the tail end of that trend; by the 1990s Japan entered a prolonged 
recession, the German economy slowed under the costs of the reunification of West and East 
Germany, and the American economy prospered again. You may be more familiar with a 
reincarnation of this trend, in the 2000s and early 2010s, this time focused on China.
James Fallows, How the World Works, The Atlantic (December 1993)
[This is an excerpt from the article, which is available at: 
https://www.theatlantic.com/magazine/archive/1993/12/how-the-world-works/305854/]
In Japan in the springtime of 1992 a trip to Hitotsubashi University, famous for its economics and 
business faculties, brought me unexpected good luck. Like several other Japanese universities, 
Hitotsubashi is almost heartbreaking in its cuteness. The road from the station to the main campus 
is lined with cherry trees, and my feet stirred up little puffs of white petals. Students glided along 
on their bicycles, looking as if they were enjoying the one stress-free moment of their lives.
They probably were. In surveys huge majorities of students say that they study "never" or "hardly 
at all" during their university careers. They had enough of that in high school.
I had gone to Hitotsubashi to interview a professor who was making waves. Since the end of the 
Second World War, Japanese diplomats and businessmen have acted as if the American economy 
should be the model for Japan's own industrial growth. Not only should Japanese industries try to 
catch up with America's lead in technology and production but also the nation should evolve 
toward a standard of economic maturity set by the United States. Where Japan's economy differed 
from the American model—for instance, in close alliances between corporations which U.S. 
antitrust laws would forbid—the difference should be considered temporary, until Japan caught 
up. 
Through the 1980s a number of foreign observers challenged this assumption, saying that Japan's 
economy might not necessarily become more like America's with the passing years. Starting in 
1990 a number of Japanese businessmen and scholars began publicly saying the same thing, 
suggesting that Japan's business system might be based on premises different from those that 
prevailed in the West. Professor Iwao Nakatani, the man I went to Hitotsubashi to meet, was one 
of the most respected members of this group, and I spent the afternoon listening to his argument 
while, through the window I watched petals drifting down.
On the way back to the station I saw a bookstore sign advertising Western-language books for sale. 
I walked to the back of the narrow store and for the thousandth time felt both intrigued and 
embarrassed by the consequences of the worldwide spread of the English language. In row upon 
row sat a jumble of books that had nothing in common except that they were published in English. 
Self-help manuals by Zig Ziglar. Bodice-rippers from the Harlequin series. A Betty Crocker 
cookbook. The complete works of Sigmund Freud. One book by, and another about, Friedrich List.
Friedrich List! For at least five years I'd been scanning used-book stores in Japan and America 
looking for just these books, having had no luck in English-language libraries. I'd scoured stores 
in Taiwan that specialized in pirated reprints of English-language books for about a tenth their 
original cost. I'd called the legendary Strand bookstore, in Manhattan, from my home in Kuala 
Lumpur, begging them to send me a note about the success of their search (it failed) rather than 
make me wait on hold. In all that time these were the first books by or about List I'd actually laid 
eyes on.
One was a biography, by a professor in the north of England. The other was a translation, by the 
same professor, of a short book List had written in German. Both were slim volumes, which, 
judging by the dust on their covers, had been on the shelf for years. I gasped when I opened the 
first book's cover and saw how high the price was—9,500 yen, about $75. For the set? I asked 
hopefully. No, apiece, the young woman running the store told me. Books are always expensive 
in Japan, but even so this seemed steep. No doubt the books had been priced in the era when one 
dollar was worth twice as many yen as it was by the time I walked into the store. I opened my 
wallet, pulled out a 10,000-yen note, took my change and the biography, and left the store. A few 
feet down the sidewalk I turned around, walked back to the store, and used the rest of my money 
to buy the other book. I would always have regretted passing it up.
Why Friedrich List? The more I had heard about List in the preceding five years, from economists 
in Seoul and Osaka and Tokyo, the more I had wondered why I had virtually never heard of him 
while studying economics in England and the United States. By the time I saw his books in the 
shop beneath the cherry trees, I had come to think of him as the dog that didn't bark. He illustrated 
the strange self-selectivity of Anglo-American thinking about economics.
I emphasize "Anglo-American" because in this area the United Kingdom and the United States are 
like each other and different from most of the rest of the world. The two countries have dominated 
world politics for more than a century, and the dominance of the English language lets them ignore 
what is being said and thought overseas—and just how isolated they have become. The difference 
shows up this way: The Anglo-American system of politics and economics, like any system, rests 
on certain principles and beliefs. But rather than acting as if these are the best principles, or the 
ones their societies prefer, Britons and Americans often act as if these were the only possible 
principles and no one, except in error, could choose any others. Political economics becomes an 
essentially religious question, subject to the standard drawback of any religion—the failure to 
understand why people outside the faith might act as they do.
To make this more specific: Today's Anglo-American world view rests on the shoulders of three 
men. One is Isaac Newton, the father of modern science. One is Jean-Jacques Rousseau, the father 
of liberal political theory. (If we want to keep this purely Anglo-American, John Locke can serve 
in his place.) And one is Adam Smith, the father of laissez-faire economics. From these founding 
titans come the principles by which advanced society, in the Anglo-American view, is supposed 
to work. A society is supposed to understand the laws of nature as Newton outlined them. It is 
supposed to recognize the paramount dignity of the individual, thanks to Rousseau, Locke, and 
their followers. And it is supposed to recognize that the most prosperous future for the greatest 
number of people comes from the free workings of the market. So Adam Smith taught, with axioms 
that were enriched by David Ricardo, Alfred Marshall, and the other giants of neoclassical 
economics.
The most important thing about this summary is the moral equivalence of the various principles. 
Isaac Newton worked in the realm of fundamental science. Without saying so explicitly, today's 
British and American economists act as if the economic principles they follow had a similar hard, 
provable, undebatable basis. If you don't believe in the laws of physics—actions create reactions, 
the universe tends toward greater entropy—you are by definition irrational. And so with 
economics. If you don't accept the views derived from Adam Smith—that free competition is 
ultimately best for all participants, that protection and interference are inherently wrong—then you 
are a flat-earther.
Outside the United States and Britain the matter looks quite different. About science there is no 
dispute. "Western" physics is the physics of the world. About politics there is more debate: with 
the rise of Asian economies some Asian political leaders, notably Lee Kuan Yew, of Singapore, 
and several cautious figures in Japan, have in effect been saying that Rousseau's political 
philosophy is not necessarily the world's philosophy. Societies may work best, Lee and others have 
said, if they pay less attention to the individual and more to the welfare of the group.
But the difference is largest when it comes to economics. In the non-Anglophone world Adam 
Smith is merely one of several theorists who had important ideas about organizing economies. In 
most of East Asia and continental Europe the study of economics is less theoretical than in England 
and America (which is why English-speakers monopolize Nobel Prizes) and more geared toward 
solving business problems.
In Japan economics has in effect been considered a branch of geopolitics—that is, as the key to 
the nation's strength or vulnerability in dealing with other powers. From this practical-minded 
perspective English-language theorists seem less useful than their challengers, such as Friedrich 
List.
Two Clashing World Views
Britons and Americans tend to see the past two centuries of economics us one long progression 
toward rationality and good sense. In 1776 Adam Smith's The Wealth of Nations made the case 
against old-style mercantilism, just as the Declaration of Independence made the case against oldstyle feudal and royal domination. Since then more and more of the world has come to the correct 
view—or so it seems in the Anglo-American countries. Along the way the world has met such 
impediments as neo-mercantilism, radical unionism, sweeping protectionism, socialism, and, of 
course, communism. One by one the worst threats have given way. Except for a few lamentable 
areas of backsliding, the world has seen the wisdom of Adam Smith's ways.
Yet during this whole time there has been an alternative school of thought. The Enlightenment 
philosophers were not the only ones to think about how the world should be organized. During the 
eighteenth and nineteenth centuries the Germans were also active—to say nothing of the theorists 
at work in Tokugawa Japan, late imperial China, czarist Russia, and elsewhere.
The Germans deserve emphasis—more than the Japanese, the Chinese, the Russians, and so on 
because many of their philosophies endure. These did not take root in England or America, but 
they were carefully studied, adapted, and applied in parts of Europe and Asia, notably Japan. In 
place of Rousseau and Locke the Germans offered Hegel. In place of Adam Smith they had 
Friedrich List.
The German economic vision differs from the Anglo-American in many ways, but the crucial 
differences are these:
* "Automatic" growth versus deliberate development. The Anglo-American approach emphasizes 
the unpredictability and unplannability of economics. Technologies change. Tastes change. 
Political and human circumstances change. And because life is so fluid, attempts at central 
planning are virtually doomed to fail. The best way to "plan," therefore is to leave the adaptation 
to the people who have their own money at stake. These are the millions of entrepreneurs who 
make up any country's economy. No planning agency could have better information than they 
about the direction things are moving, and no one could have a stronger incentive than those who 
hope to make a profit and avoid a loss. By the logic of the Anglo-American system, if each 
individual does what is best for him or her, the result will be what is best for the nation as a whole.
Although List and others did not use exactly this term, the German school was more concerned 
with "market failures." In the language of modern economics these are the cases in which normal 
market forces produce a clearly undesirable result. The standard illustration involves pollution. If 
the law allows factories to dump pollutants into the air or water, then every factory will do so. 
Otherwise, their competitors will have lower costs and will squeeze them out. This "rational" 
behavior will leave everyone worse off. The answer to such a market failure is for the society—
that is, the government—to set standards that all factories must obey.
Friedrich List and his best-known American counterpart, Alexander Hamilton, argued that 
industrial development entailed a more sweeping sort of market failure. Societies did not 
automatically move from farming to small crafts to major industries just because millions of small 
merchants were making decisions for themselves. If every person put his money where the return 
was greatest, the money might not automatically go where it would do the nation the most good. 
For it to do so required a plan, a push, an exercise of central power. List drew heavily on the history 
of his times—in which the British government deliberately encouraged British manufacturing and 
the fledgling American government deliberately discouraged foreign competitors.
This is the gist of List's argument, from The Natural System of Political Economy, which he wrote 
in five weeks in 1837:
The cosmopolitan theorists [List's term for Smith and his ilk] do not question the 
importance of industrial expansion. They assume, however, that this can be achieved by 
adopting the policy of free trade and by leaving individuals to pursue their own private 
interests. They believe that in such circumstances a country will automatically secure the 
development of those branches of manufacture which are best suited to its own particular 
situation. They consider that government action to stimulate the establishment of industries 
does more harm than good....
The lessons of history justify our opposition to the assertion that states reach economic 
maturity most rapidly if left to their own devices. A study of the origin of various branches 
of manufacture reveals that industrial growth may often have been due to chance. It may 
be chance that leads certain individuals to a particular place to foster the expansion of an 
industry that was once small and insignificant—just as seeds blown by chance by the wind 
may sometimes grow into big trees. But the growth of industries is a process that may take 
hundreds of years to complete and one should not ascribe to sheer chance what a nation 
has achieved through its laws and institutions. In England Edward III created the 
manufacture of woolen cloth and Elizabeth founded the mercantile marine and foreign 
trade. In France Colbert was responsible for all that a great power needs to develop its 
economy. Following these examples every responsible government should strive to remove 
those obstacles that hinder the progress of civilisation and should stimulate the growth of 
those economic forces that a nation carries in its bosom. 
* Consumers versus producers. The Anglo-American approach assumes that the ultimate measure 
of a society is its level of consumption. Competition is good, because it kills off producers whose 
prices are too high. Killing them off is good, because more-efficient suppliers will give the 
consumer a better deal. Foreign trade is very good, because it means that the most efficient 
suppliers in the whole world will be able to compete. It doesn't even matter why competitors are 
willing to sell for less. They may really be more efficient; they may be determined to dump their 
goods for reasons of their own. In either case the consumer is better off. He has the ton of steel, 
the cask of wine, or—in today's terms—the car or computer that he might have bought from a 
domestic manufacturer, plus the money he saved by buying foreign goods.
In the Friedrich List view, this logic leads to false conclusions. In the long run, List argued, a 
society's well-being and its overall wealth are determined not by what the society can buy but by 
what it can make. This is the corollary of the familiar argument about foreign aid: Give a man a 
fish and you feed him for a day. Teach him how to fish and you feed him for his life.
List was not concerned here with the morality of consumption. Instead he was interested in both 
strategic and material well-being. In strategic terms nations ended up being dependent or 
independent according to their ability to make things for themselves. Why were Latin Americans, 
Africans, and Asians subservient to England and France in the nineteenth century? Because they 
could not make the machines and weapons Europeans could.
In material terms a society's wealth over the long run is greater if that society also controls 
advanced activities. That is, if you buy the ton of steel or cask of wine at bargain rates this year, 
you are better off, as a consumer, right away. But over ten years, or fifty, you and your children 
may be stronger as both consumers and producers if you learn how to make the steel and wine 
yourself. If you can make steel rather than just being able to buy it, you'll be better able to make 
machine tools. If you're able to make machine tools, you'll be better able to make engines, robots, 
airplanes. If you're able to make engines and robots and airplanes, your children and grandchildren 
will be more likely to make advanced products and earn high incomes in the decades ahead.
The German school argued that emphasizing consumption would eventually be self-defeating. It 
would bias the system away from wealth creation—and ultimately make it impossible to consume 
as much. To use a homely analogy: One effect of getting regular exercise is being able to eat more 
food, just as an effect of steadily rising production is being able to consume more. But if people 
believe that the reason to get exercise is to permit themselves to eat more, rather than for longer 
term benefits they will behave in a different way. List's argument was that developing productive 
power was in itself a reward. "The forces of production are the tree on which wealth grows," List 
wrote in another book, called The National System of Political Economy.
The tree which bears the fruit is of greater value than the fruit itself.... The prosperity of a 
nation is not ... greater in the proportion in which it has amassed more wealth (ie, values of 
exchange), but in the proportion in which it has more developed its powers of production. 
* Process versus result. In economics and politics alike the Anglo-American theory emphasizes 
how the game is played, not who wins or loses. If the rules are fair, then the best candidate will 
win. If you want better politics or a stronger economy, you should concentrate on reforming the 
rules by which political and economic struggles are waged. Make sure everyone can vote; make 
sure everyone can bring new products to market. Whatever people choose under those fair rules 
will by definition be the best result. Abraham Lincoln or Warren Harding, Shakespeare or 
Penthouse—in a fair system whatever people choose will be right.
The government's role, according to this outlook, is not to tell people how they should pursue 
happiness or grow rich. Rather, its role is that of referee—making sure no one cheats or bends the 
rules of "fair play," whether by voter fraud in the political realm or monopoly in the economic.
In the late twentieth century the clearest practical illustration of this policy has been the U.S. 
financial market. The government is actively involved—but only to guard the process, not to steer 
the results. It runs elaborate sting operations to try to prevent corporate officials from trading on 
inside information. It requires corporations to publish detailed financial reports every quarter, so 
that all investors will have the same information to work from. It takes companies to court—IBM, 
AT&T—whenever they seem to be growing too strong and stunting future competitors. It exposes 
pension-fund managers to punishment if they do not invest their assets where the dividends are 
greatest.
These are all ways of ensuring that the market will "get prices right," as economists say, so that 
investments will flow to the best possible uses. Beyond that it is up to the market to decide where 
the money goes. Short-term loans to cover the budget deficits in Mexico or the United States? 
Fine. Long-term investments in cold-fusion experimentation? Fine. The market will automatically 
assign each prospect the right price. If fusion engines really would revolutionize the world, then 
investors will voluntarily risk their money there.
The German view is more paternalistic. People might not automatically choose the best society or 
the best use of their money. The state, therefore, must be concerned with both the process and the 
result. Expressing an Asian variant of the German view, the sociologist Ronald Dore has written 
that the Japanese—"like all good Confucianists"—believe that "you cannot get a decent, moral 
society, not even an efficient society, simply out of the mechanisms of the market powered by the 
motivational fuel of self-interest." So, in different words, said Friedrich List.
* Individuals versus the nation. The Anglo-American view focuses on how individuals fare as 
consumers and on how the whole world fares as a trading system. But it does not really care about 
the intermediate levels between one specific human being and all five billion—that is, about 
communities and nations.
This criticism may seem strange, considering that Adam Smith called his mighty work The Wealth 
of Nations. It is true that Smith was more of a national-defense enthusiast than most people who 
now invoke his name. For example, he said that the art of war was the "noblest" of the arts, and he 
approved various tariffs that would keep defense-related industries strong—which in those days 
meant sailcloth making. He also said that since defense "is of much more importance than 
opulence, the act of navigation is, perhaps, the wisest of all the commercial regulations of 
England." This "act of navigation" was, of course, the blatantly protectionist legislation designed 
to restrict the shipment of goods going to and from England mostly to English ships.
Still, the assumption behind the Anglo-American model is that if you take care of the individuals, 
the communities and nations will take care of themselves. Some communities will suffer, as dying 
industries and inefficient producers go down, but other communities will rise. And as for nations 
as a whole, outside the narrow field of national defense they are not presumed to have economic 
interests. There is no general "American" or "British" economic interest beyond the welfare of the 
individual consumers who happen to live in America or Britain.
The German view is more concerned with the welfare, indeed sovereignty, of people in groups—
in communities, in nations. This is its most obvious link with the Asian economic strategies of 
today. Friedrich List fulminated against the "cosmopolitan theorists," like Adam Smith, who 
ignored the fact that people lived in nations and that their welfare depended to some degree on 
how their neighbors fared. In the real world happiness depends on more than how much money 
you take home. If the people around you are also comfortable (though, ideally, not as comfortable 
as you), you are happier and safer than if they are desperate. This, in brief, is the case that today's 
Japanese make against the American economy: American managers and professionals live more 
opulently than their counterparts in Japan, but they have to guard themselves, physically and 
morally, against the down-and-out people with whom they share the country.
In the German view, the answer to this predicament is to pay explicit attention to the welfare of 
the nation. If a consumer has to pay 10 percent more for a product made by his neighbors than for 
one from overseas, it will be worse for him in the short run. But in the long run, and in the broadest 
definitions of well-being, he might be better off. As List wrote in The National System of Political 
Economy
Between each individual and entire humanity, however, stands the NATION, with its 
special language and literature, with its peculiar origin and history, with its special manners 
and customs, laws and institutions, with the claims of all these for existence, independence, 
perfection, and continuance for the future, and with its separate territory; a society which, 
united by a thousand ties of mind and of interests, combines itself into one independent 
whole. 
Economic policies, in the German view, will be good or bad depending on whether they take into 
account this national economic interest. Which leads to
* Business as peace versus business as war. By far the most uplifting part of the Anglo-American 
view is the idea that everyone can prosper at once. Before Adam Smith, the Spanish and Portuguese 
mercantilists viewed world trade as a kind of battle. What I won, you lost. Adam Smith and David 
Ricardo demonstrated that you and I could win at the same time. If I bought your wine and you 
bought my wool, we would both have more of what we wanted, for the same amount of work. The 
result would be the economist's classic "positive sum" interaction. Your well-being and my wellbeing added together would be greater than they were before our trade.
The Germans had a more tragic, or "zero sum"-like, conception of how nations dealt with each 
other. Some won; others lost. Economic power often led to political power, which in turn let one 
nation tell others what to do. Since the Second World War, American politicians have often said 
that their trading goal is a "level playing field" for competition around the world. This very image 
implies a horizontal relationship among nations, in which they all good-naturedly joust as more or 
less equal rivals. "These horizontal metaphors are fundamentally misleading," the American writer 
John Audis has written in the magazine In These Times.
Instead of being grouped horizontally on a flat field, nations have always been organized 
vertically in a hierarchical division of labor. The structure of the world economy more 
accurately resembles a pyramid or a cone rather than a plane. In the 17th century, the Dutch 
briefly stood atop the pyramid. Then, after a hundred year transition during which the 
British and French vied for supremacy, the British emerged in 1815 as the world's leading 
industrial and financial power, maintaining their place through the end of the century. 
Then, after about a forty-year transition, the U.S. came out of World War II on top of the 
pyramid. Now we are in a similar period of transition from which it is likely, after another 
two decades, that Japan will emerge as the leading industrial power. 
The same spirit and logic run through List's arguments. Trade is not just a game. Over the long 
sweep of history some nations lose independence and control of their destiny if they fall behind in 
trade. Therefore nations must think about it strategically, not just as a matter of where they can 
buy the cheapest shirt this week.
In The Natural System of Political Economy, List included a chapter on this theme, "The Dominant 
Nation." Like many other things written about Britain in the nineteenth century, it makes 
bittersweet reading for twentieth-century Americans. "England's manufactures are based upon 
highly efficient political and social institutions, upon powerful machines, upon great capital 
resources, upon an output larger than that of all other countries, and upon a complete network of 
internal transport facilities," List said of the England of the 1830s, as many have said of the United 
States of the 1950s and 1960s.
A nation which makes goods more cheaply than anyone else and possesses immeasurably 
more capital than anyone else is able to grant its customers more substantial and longer 
credits than anyone else....By accepting or by excluding the import of their raw materials 
and other products, England—all powerful as a manufacturing and commercial country—
can confer great benefits or inflict great injuries upon nations with relatively backward 
economies.
This is what England lost when it lost "dominance," and what Japan is gaining now.
* Morality versus power. By now the Anglo-American view has taken on a moral tone that was 
embryonic when Adam Smith wrote his book. If a country disagrees with the Anglo-American 
axioms, it doesn't just disagree: it is a "cheater." Japan "cheats" the world trading system by 
protecting its rice farmers. America "cheats" with its price supports for sugar-beet growers and its 
various other restrictions on trade. Malaysia "cheated" by requiring foreign investors to take on 
local partners. And on and on. If the rules of the trading system aren't protected from such cheating, 
the whole system might collapse and bring back the Great Depression.
In the German view, economics is not a matter of right or wrong, or cheating or playing fair. It is 
merely a matter of strong or weak. The gods of trade will help those who help themselves. No code 
of honor will defend the weak, as today's Latin Americans and Africans can attest. If a nation 
decides to help itself—by protecting its own industries, by discriminating against foreign 
products—then that is a decision, not a sin. […]
* * *
Dodge v. Ford Motor Co., 170 N.W. 668 (Mich. 1919)
[The Ford Motor Company (“FMC”) was founded in 1903 by a number of investors, including 
Henry Ford and brothers John F. Dodge and Horace E. Dodge (“the Dodge brothers”). Henry 
Ford, who held a 58% interest in FMC, was also FMC’s President and a director on its board. The 
Dodge brothers held a 10% interest, were not on the board of directors nor employed by FMC.
FMC’s business strategy was focused on mass-market cars that were lower priced but appealed to 
a larger group of potential customers. To afford to sell cars at a low price, FMC focused on mass 
production of cars and vertical integration (owning the businesses that produced the raw materials 
needed to produce cars). These allowed it to continuously reduce the cost of its cars, and the lower 
costs allowed selling the car at a lower price, making its cars affordable to customers who were 
previously priced-out. For example, according to Wikipedia, the standard Model T 4-seat open 
tourer of 1909 cost $850 (equivalent to $20,513 today). The price dropped to $550 in 1913 
(equivalent to $12,067 today); to $440 in 1915 (equivalent to $9,431 today); and to $290 
(equivalent to $3,258 today) in the 1920s.
Beginning in 1911, regular annual dividends were $1.2M. In addition, between 1913 and 1915 
the company paid special dividends of $10-11M each year. Then, in 1916, Henry Ford announced 
that FMC would no longer pay special dividends and that profits would be retained to pay for the 
new River Rouge plant, which will allow FMC to expand its production capacity; to double 
employees’ salaries; and to cut the price of cars.
The Dodge brothers sued: (1) for a decree requiring FMC to distribute to stockholders at least 75% 
of the accumulated cash surplus, and to distribute in the future all of its earnings “except such as 
may be reasonably required for emergency purposes”; and (2) to enjoin the construction of the 
River Rouge plant.]
[…] [The court rejects plaintiffs’ arguments that FMC violated a state law ceiling on a 
corporation’s capital; that FMC exceeded the activities it was authorized to conduct (ultra vires); 
or that FMC violated antitrust laws.]
As we regard the testimony as failing to prove any violation of anti-trust laws or that the alleged 
policy of the company, if successfully carried out, will involve a monopoly other than such as 
accrues to a concern which makes what the public demands and sells it at a price which the public 
regards as cheap or reasonable, the case for plaintiffs must rest upon the claim, and the proof in 
support of it, that the proposed expansion of the business of the corporation, involving the further 
use of profits as capital, ought to be enjoined because inimical to the best interests of the company 
and its shareholders, and upon the further claim that in any event the withholding of the special 
dividend asked for by plaintiffs is arbitrary action of the directors requiring judicial interference.
The rule which will govern courts in deciding these questions is not in dispute. […] This court, in 
Hunter v. Roberts, Throp & Co., recognized the rule in the following language:
It is a well-recognized principle of law that the directors of a corporation, and they alone, 
have the power to declare a dividend of the earnings of the corporation, and to determine 
its amount. Courts of equity will not interfere in the management of the directors unless it 
is clearly made to appear that they are guilty of fraud or misappropriation of the corporate 
funds, or refuse to declare a dividend when the corporation has a surplus of net profits 
which it can, without detriment to its business, divide among its stockholders, and when a 
refusal to do so would amount to such an abuse of discretion as would constitute a fraud, 
or breach of that good faith which they are bound to exercise towards the stockholders.
In Cook on Corporations (7th Ed.) §545, it is expressed as follows:
The board of directors declare the dividends, and it is for the directors, and not the 
stockholders, to determine whether or not a dividend shall be declared. When, therefore, 
the directors have exercised this discretion and refused to declare a dividend, there will be 
no interference by the courts with their decision, unless they are guilty of a willful abuse 
of their discretionary powers, or of bad faith or of a neglect of duty. It requires a very strong 
case to induce a court of equity to order the directors to declare a dividend, inasmuch as 
equity has no jurisdiction, unless fraud or a breach of trust is involved. There have been 
many attempts to sustain such a suit, yet, although the courts do not disclaim jurisdiction, 
they have quite uniformly refused to interfere. The discretion of the directors will not be 
interfered with by the courts, unless there has been bad faith, willful neglect, or abuse of 
discretion. Accordingly, the directors may, in the fair exercise of their discretion, invest 
profits to extend and develop the business, and a reasonable use of the profits to provide 
additional facilities for the business cannot be objected to or enjoined by the stockholders.
[…] One other statement may be given from Park v. Grant Locomotive Works:
In cases where the power of the directors of a corporation is without limitation, and free 
from restraint, they are at liberty to exercise a very liberal discretion as to what disposition 
shall be made of the gains of the business of the corporation. Their power over them is 
absolute so long as they act in the exercise of their honest judgment. They may reserve of 
them whatever their judgment approves as necessary or judicious for repairs or 
improvements, and to meet contingencies, both present and prospective. And their 
determination in respect of these matters, if made in good faith and for honest ends, though 
the result may show that it was injudicious, is final, and not subject to judicial revision.
[…] When plaintiffs made their complaint and demand for further dividends, the Ford Motor 
Company had concluded its most prosperous year of business. The demand for its cars at the price 
of the preceding year continued. It could make and could market in the year beginning August 1, 
1916, more than 500,000 cars. […] It had declared no special dividend during the business year 
except the October 1915, dividend. It had been the practice, under similar circumstances, to declare 
larger dividends. Considering only these facts, a refusal to declare and pay further dividends 
appears to be not an exercise of discretion on the part of the directors, but an arbitrary refusal to 
do what the circumstances required to be done. These facts and others call upon the directors to 
justify their action, or failure or refusal to act.
In justification, the defendants have offered testimony tending to prove, and which does prove, the 
following facts: It had been the policy of the corporation for a considerable time to annually reduce 
the selling price of cars, while keeping up, or improving, their quality. As early as in June 1915, a 
general plan for the expansion of the productive capacity of the concern by a practical duplication 
of its plant had been talked over by the executive officers and directors and agreed upon; not all of 
the details having been settled, and no formal action of directors having been taken. The erection 
of a smelter was considered, and engineering and other data in connection therewith secured. In 
consequence, it was determined not to reduce the selling price of cars for the year beginning 
August 1, 1915, but to maintain the price and to accumulate a large surplus to pay for the proposed 
expansion of plant and equipment, and perhaps to build a plant for smelting ore. It is hoped, by 
Mr. Ford, that eventually 1,000,000 cars will be annually produced. The contemplated changes 
will permit the increased output.
The plan […] calls for a reduction in the selling price of the cars. [… T]he plan does not call for 
and is not intended to produce immediately a more profitable business, but a less profitable one; 
not only less profitable than formerly, but less profitable than it is admitted it might be made. The 
apparent immediate effect will be to diminish the value of shares and the returns to shareholders.
It is the contention of plaintiffs that the apparent effect of the plan is […] to continue the 
corporation henceforth as a semi-eleemosynary institution and not as a business institution. In 
support of this contention, they point to the attitude and to the expressions of Mr. Henry Ford.
Mr. Henry Ford is the dominant force in the business of the Ford Motor Company. No plan of 
operations could be adopted unless he consented, and no board of directors can be elected whom 
he does not favor. […] ‘My ambition,’ said Mr. Ford, ‘is to employ still more men, to spread the 
benefits of this industrial system to the greatest possible number, to help them build up their lives 
and their homes. To do this we are putting the greatest share of our profits back in the business.’ 
[…]
He had made up his mind in the summer of 1916 that no dividends other than the regular dividends 
should be paid, ‘for the present.’
‘Q. For how long? Had you fixed in your mind any time in the future, when you were going 
to pay-- A. No.
‘Q. That was indefinite in the future? A. That was indefinite; yes, sir.’
The record, and especially the testimony of Mr. Ford, convinces that he has to some extent the 
attitude towards shareholders of one who has dispensed and distributed to them large gains and 
that they should be content to take what he chooses to give. His testimony creates the impression, 
also, that he thinks the Ford Motor Company has made too much money, has had too large profits, 
and that, although large profits might be still earned, a sharing of them with the public, by reducing 
the price of the output of the company, ought to be undertaken. We have no doubt that certain 
sentiments, philanthropic and altruistic, creditable to Mr. Ford, had large influence in determining 
the policy to be pursued by the Ford Motor Company – the policy which has been herein referred 
to.
[…] There should be no confusion (of which there is evidence) of the duties which Mr. Ford 
conceives that he and the stockholders owe to the general public and the duties which in law he 
and his codirectors owe to protesting, minority stockholders. A business corporation is organized 
and carried on primarily for the profit of the stockholders. The powers of the directors are to be 
employed for that end. The discretion of directors is to be exercised in the choice of means to attain 
that end, and does not extend to a change in the end itself, to the reduction of profits, or to the 
nondistribution of profits among stockholders in order to devote them to other purposes.
There is committed to the discretion of directors, a discretion to be exercised in good faith, the 
infinite details of business, including the wages which shall be paid to employees, the number of 
hours they shall work, the conditions under which labor shall be carried on, and the price for which 
products shall be offered to the public.
It is said by appellants that the motives of the board members are not material and will not be 
inquired into by the court so long as their acts are within their lawful powers. As we have pointed 
out, […] it is not within the lawful powers of a board of directors to shape and conduct the affairs 
of a corporation for the merely incidental benefit of shareholders and for the primary purpose of 
benefiting others, and no one will contend that, if the avowed purpose of the defendant directors 
was to sacrifice the interests of shareholders, it would not be the duty of the courts to interfere.
We are not, however, persuaded that we should interfere with the proposed expansion of the 
business of the Ford Motor Company. [… T]he ultimate results of the larger business cannot be 
certainly estimated. The judges are not business experts. It is recognized that plans must often be 
made for a long future, for expected competition, for a continuing as well as an immediately 
profitable venture. The experience of the Ford Motor Company is evidence of capable 
management of its affairs.
It may be noticed, incidentally, that it took from the public the money required for the execution 
of its plan, and that the very considerable salaries paid to Mr. Ford and to certain executive officers 
and employees were not diminished. We are not satisfied that the alleged motives of the directors, 
in so far as they are reflected in the conduct of the business, menace the interests of shareholders. 
It is enough to say, perhaps, that the court of equity is at all times open to complaining shareholders 
having a just grievance.
[…] Defendants say, and it is true, that a considerable cash balance must be at all times carried by 
such a concern. But, as has been stated, there was a large daily, weekly, monthly, receipt of cash. 
The output was practically continuous and was continuously, and within a few days, turned into 
cash. Moreover, the contemplated expenditures were not to be immediately made. The large sum 
appropriated for the smelter plant was payable over a considerable period of time. So that, without 
going further, it would appear that, accepting and approving the plan of the directors, it was their 
duty to distribute on or near the 1st of August, 1916, a very large sum of money to stockholders.
[The court upholds the lower court’s decree that a dividend must be paid, but reverses the lower 
court’s injunction against building the smelting plant.]
Class 2: Shareholders versus Directors (Blasius Industries, Inc. v. Atlas Corp.)
Dodge was a philosophical case about an abstract principle: what’s the corporation’s purpose? In 
contrast, Blasius is a down-to-earth case about the technical details of how shareholders and 
directors battle over what the corporation does. It is one of my favorite cases in my Mergers & 
Acquisitions course.
Delaware corporate law strikes a particular balance on the issue of the corporation’s purpose: the 
corporation needs to be operated to maximize shareholders’ wealth, but the board of directors is 
given wide discretion to determine what that interest is.
What can shareholders do when they don’t like the board’s interpretation of their interests? They 
can sell their shares, but that doesn’t directly change the board’s behavior (though it could lower 
directors’ compensation if that compensation is tied to the firm’s stock price). They can sue the 
directors, but as I said above, Delaware law gives broad discretion for directors to decide what is 
in the shareholders’ interest, as long as there is no evidence that directors are self-dealing 
(enriching themselves at the shareholders’ expense). Finally, shareholders can vote to remove and 
replace the directors, or to increase the size of the board and add more (shareholder-friendly) 
directors to the board.
Blasius is an excellent case for examining what shareholders can do against directors when they 
are unhappy with directors’ decisions, and also what directors can do to thwart the shareholders. 
You can think of the case as the first draft of the “Activist shareholder’s playbook” as well as the 
“Directors’ manual of defense against activists”. To help you understand the case, I need to discuss
some nitty-gritty technical details of corporate governance.
Shareholders can act in one of two ways: by calling a shareholder meeting, or by written consent. 
A corporation is only required to hold one shareholder meeting per year – the annual shareholder 
meeting. If shareholders have to wait for the annual meeting, the conflict between them and the 
directors may already be resolved in the directors’ favor (e.g., a third party offer that the 
shareholders want the firm to accept will have expired; or the board will have time to take actions 
that make the firm unappealing to the third party). So waiting for the annual meeting is 
shareholders’ last resort.
Additional shareholder meetings (called special shareholder meetings) may be called, but in most 
Delaware public corporations only the board of directors, not the shareholders, may call special 
meetings. Naturally, the board won’t call a meeting that would allow shareholders to impose their 
will on the board, so special shareholder meetings are only a viable tool if the corporation’s bylaws 
or charter allow shareholders to call them.
A written consent is a written document that shareholders sign on to. Unless prohibited by the 
corporation’s charter, a written consent is considered the valid act of the shareholders if the 
appropriate majority of shareholders signed it. The appropriate majority being whatever majority 
would have been needed to take the same action in a meeting in which all shareholders attended. 
In the case of replacing a director or changing the corporation’s bylaws, this would be a 50% plus 
one vote). Written consents have another potential advantage over meetings: meetings require 
advance notification that alerts the directors to the shareholders’ plan (which gives time for the 
board to respond). In contrast, a written consent, if it is kept secret from the board, can be sprung 
on them as a surprise after the required majority of shareholders signed it, in which case the 
shareholder action is already a done deal.
For those reasons, the shareholders in Blasius chose to act through a written consent.
Once you figure out how to act, the next question is what the action should be. Directors can 
always be removed for cause (i.e., if they acted in a wrongful way), but they can stall the process 
by litigating that there was no cause to remove them. Under some circumstances, directors can 
also be removed by shareholders without cause, but it appears this was not an option in the Blasius
case.
The shareholders in the Blasius case came up with an original alternative: They planned to increase
the size of the board, thereby creating vacancies on the board (spots to which a director has not yet 
been elected). And they then planned to immediately fill the vacancies with shareholder-friendly 
new directors. After doing this, the board would still include the original directors, but if 
shareholders appointed enough new directors, those new directors will have the majority of votes 
on the board. 
The shareholders had to act fast: both shareholders and the board have the power to fill board 
vacancies, so if the shareholders did not fill the vacancies in the same written consent that created 
the vacancies (by increasing the board’s size), the board would no doubt fill those vacancies 
immediately (with new directors who support the board’s views, not the shareholders’ views). Not 
surprisingly, the shareholders in Blasius use the same written consent to both increase the size of 
the board and to fill the vacancies.
Is there any limit to shareholders’ ability to increase the board’s size? There might be. The board’s 
size can be determined in the corporation’s charter, in its bylaws (as long as they don’t contradict 
the charter), or the charter may delegate to the board to determine its size in a board decision. The 
charter can only be changed by a joint action of both shareholder and directors, so any limits on 
board size that are in the charter cannot be changed unilaterally by shareholders. In contrast, 
bylaws can be changed by unilateral action of either the board or the shareholders, so if the board 
size was determined in the bylaws, shareholders could change it unilaterally. If the charter had 
delegated this task to the board, shareholders could do nothing and their plan could not succeed.
In Blasius, the charter of the relevant corporation (Atlas) said that the board will be of whatever 
size the bylaws say it is, but no more than 15 people. The bylaws then stated that the number of 
directors is 7. So shareholders could unilaterally change board size, but no higher than 15. 
Unsurprisingly, this is what they tried to do.
But the shareholders lost the element of surprise when word leaked to the board that shareholders 
were preparing to take over the board by written consent. The board then fought back. I won’t 
spoil the plot for you by telling you what the board did – you’ll see when you read the case, below. 
Suffice to say that it thwarted the shareholders’ plan, and the shareholders sued, claiming that the 
board’s actions breached their fiduciary duties.
As I mentioned earlier, directors have a very broad discretion to determine what’s in the 
shareholders’ interests, even when shareholders say they want something else. But this is not a 
typical case; in Blasius, shareholders were not giving their opinion on how to run the corporation 
(which is the board’s job and shareholders have no right to dictate); rather, they were using their 
legal right to act through a written consent, change bylaws and appoint directors to vacancies. In 
thwarting these actions, aren’t directors violating shareholders’ rights?
An alternative for the court was to apply the standard it usually applies when directors are selfdealing (e.g., enriching themselves at shareholders’ expense). In such cases, the court uses its own 
judgement as to what’s in the shareholders’ interests, and does not defer to the directors’ views. 
Courts hate to do this because they do not have the expertise to make business decisions for the 
corporation. Rather, they use the threat of doing this to deter boards from self-dealing. Expanding 
the rule to also include situations like Blasius would likely force courts to use their own discretion 
more frequently, a policy that may result in more judicial mistakes that erode the legitimacy the 
court has.
So what’s the court to do? It created a new, in-between, standard of review for situations in which 
directors thwart shareholders’ rights in order to pursue what directors paternalistically believe is 
in the shareholder’s interest. You’ll see the details in the case and we will discuss them in class.
I will also discuss in class, at length, one other aspect of this case: it is remarkably modern for a 
case that’s about 30 years old. You could see corporate battles very similar to it in today’s 
newspapers, between activist shareholders (such as some hedge funds) and boards of public 
corporations. What’s remarkable is not just that a case from 1988 seems modern, but that a case 
from, say, 1978 would not. Delaware law still relies on important precedents from the 1980s 
(especially the latter half of that decade). Yet hardly any cases from the 1970s, 1960s, or before 
are still relevant today.
Something happened in corporate America in the 1980s that changed it so dramatically that earlier 
precedents are mostly irrelevant because they address corporate realities that no longer exist. In 
contrast, we still live in a corporate world not very different from the one that developed in the 
1980s (and therefore precedents from that time are still relevant today). To better understand and 
enjoy Blasius, I will open our class with a brief lesson in economic history that will explain what 
happened in the 1980s that created a landscape of activist shareholders battling boards of directors 
– the same landscape that corporate battles are fought over today.
Blasius Industries, Inc. v. Atlas Corp., 564 A.2d 651(Del. 1988)
Two cases pitting the directors of Atlas Corporation against that company's largest (9.1%) 
shareholder, Blasius Industries, have been consolidated and tried together. Together, these cases 
ultimately require the court to determine who is entitled to sit on Atlas' board of directors. Each, 
however, presents discrete and important legal issues. [The second case was edited out.]
The first of the cases was filed on December 30, 1987. As amended, it challenges the validity of 
board action taken at a telephone meeting of December 31, 1987 that added two new members to 
Atlas' seven member board. That action was taken as an immediate response to the delivery to 
Atlas by Blasius the previous day of a form of stockholder consent that, if joined in by holders of 
a majority of Atlas' stock, would have increased the board of Atlas from seven to fifteen members 
and would have elected eight new members nominated by Blasius. […]
[Factual Background]
Blasius Acquires a 9% Stake in Atlas.
Blasius is a new stockholder of Atlas. It began to accumulate Atlas shares for the first time in July, 
1987. On October 29, it filed a Schedule 13D with the Securities Exchange Commission disclosing 
that, with affiliates, it then owed 9.1% of Atlas' common stock. It stated in that filing that it 
intended to encourage management of Atlas to consider a restructuring of the Company or other 
transaction to enhance shareholder values. It also disclosed that Blasius was exploring the 
feasibility of obtaining control of Atlas, including instituting a tender offer or seeking 
“appropriate” representation on the Atlas board of directors.
Blasius has recently come under the control of two individuals, Michael Lubin and Warren Delano, 
who after experience in the commercial banking industry, had, for a short time, run a venture 
capital operation for a small investment banking firm. Now on their own, they apparently came to 
control Blasius with the assistance of Drexel Burnham's well noted junk bond mechanism. Since 
then, they have made several attempts to effect leveraged buyouts, but without success.
In May, 1987, with Drexel Burnham serving as underwriter, Lubin and Delano caused Blasius to 
raise $60 million through the sale of junk bonds. A portion of these funds were used to acquire a 
9% position in Atlas. According to its public filings with the SEC, Blasius' debt service obligations 
arising out of the sale of the junk bonds are such that it is unable to service those obligations from 
its income from operations.
The prospect of Messrs. Lubin and Delano involving themselves in Atlas' affairs, was not a 
development welcomed by Atlas' management. Atlas had a new CEO, defendant Weaver, who 
had, over the course of the past year or so, overseen a business restructuring of a sort. Atlas had 
sold three of its five divisions. It had just announced (September 1, 1987) that it would close its 
once important domestic uranium operation. The goal was to focus the Company on its gold mining 
business. By October, 1987, the structural changes to do this had been largely accomplished. Mr. 
Weaver was perhaps thinking that the restructuring that had occurred should be given a chance to 
produce benefit before another restructuring (such as Blasius had alluded to in its Schedule 13D 
filing) was attempted, when he wrote in his diary on October 30, 1987:
13D by Delano & Lubin came in today. Had long conversation w/MAH & Mark Golden 
[of Goldman, Sachs] on issue. All agree we must dilute these people down by the 
acquisition of another Co. w/stock, or merger or something else.
The Blasius Proposal of A Leverage Recapitalization Or Sale.
Immediately after filing its 13D on October 29, Blasius' representatives sought a meeting with the 
Atlas management. Atlas dragged its feet. A meeting was arranged for December 2, 1987 
following the regular meeting of the Atlas board. Attending that meeting were Messrs. Lubin and 
Delano for Blasius, and, for Atlas, Messrs. Weaver, Devaney (Atlas' CFO), Masinter (legal counsel 
and director) and Czajkowski (a representative of Atlas' investment banker, Goldman Sachs).
At that meeting, Messrs. Lubin and Delano suggested that Atlas engage in a leveraged 
restructuring and distribute cash to shareholders. In such a transaction, which is by this date a 
commonplace form of transaction, a corporation typically raises cash by sale of assets and 
significant borrowings and makes a large one time cash distribution to shareholders. The 
shareholders are typically left with cash and an equity interest in a smaller, more highly leveraged 
enterprise. Lubin and Delano gave the outline of a leveraged recapitalization for Atlas as they saw 
it.
Immediately following the meeting, the Atlas representatives expressed among themselves an 
initial reaction that the proposal was infeasible. On December 7, Mr. Lubin sent a letter detailing 
the proposal. […]
Atlas Asks Its Investment Banker to Study the Proposal.
This written proposal was distributed to the Atlas board on December 9 and Goldman Sachs was 
directed to review and analyze it.
The proposal met with a cool reception from management. On December 9, Mr. Weaver issued a 
press release expressing surprise that Blasius would suggest using debt to accomplish what he 
characterized as a substantial liquidation of Atlas at a time when Atlas' future prospects were 
promising. He noted that the Blasius proposal recommended that Atlas incur a high debt burden 
in order to pay a substantial one time dividend consisting of $35 million in cash and $125 million 
in subordinated debentures. Mr. Weaver also questioned the wisdom of incurring an enormous 
debt burden amidst the uncertainty in the financial markets that existed in the aftermath of the 
October crash.
Blasius attempted on December 14 and December 22 to arrange a further meeting with the Atlas 
management without success. During this period, Atlas provided Goldman Sachs with projections 
for the Company. Lubin was told that a further meeting would await completion of Goldman's 
analysis. A meeting after the first of the year was proposed.
The Delivery of Blasius' Consent Statement.
On December 30, 1987, Blasius caused Cede & Co. (the registered owner of its Atlas stock) to 
deliver to Atlas a signed written consent (1) adopting a precatory resolution recommending that 
the board develop and implement a restructuring proposal, (2) amending the Atlas bylaws to, 
among other things, expand the size of the board from seven to fifteen members-the maximum 
number under Atlas' charter, and (3) electing eight named persons to fill the new directorships. 
Blasius also filed suit that day in this court seeking a declaration that certain bylaws adopted by 
the board on September 1, 1987 acted as an unlawful restraint on the shareholders' right, created 
by Section 228 of our corporation statute, to act through consent without undergoing a meeting.
The reaction was immediate. Mr. Weaver conferred with Mr. Masinter, the Company's outside 
counsel and a director, who viewed the consent as an attempt to take control of the Company. They 
decided to call an emergency meeting of the board, even though a regularly scheduled meeting 
was to occur only one week hence, on January 6, 1988. The point of the emergency meeting was 
to act on their conclusion (or to seek to have the board act on their conclusion) “that we should 
add at least one and probably two directors to the board ...”. A quorum of directors, however, could 
not be arranged for a telephone meeting that day. A telephone meeting was held the next day. At 
that meeting, the board voted to amend the bylaws to increase the size of the board from seven to 
nine and appointed John M. Devaney and Harry J. Winters, Jr. to fill those newly created positions. 
Atlas' Certificate of Incorporation creates staggered terms for directors; the terms to which Messrs. 
Devaney and Winters were appointed would expire in 1988 and 1990, respectively.
The Motivation of the Incumbent Board In Expanding the Board and Appointing New Members.
In increasing the size of Atlas' board by two and filling the newly created positions, the members 
of the board realized that they were thereby precluding the holders of a majority of the Company's 
shares from placing a majority of new directors on the board through Blasius' consent solicitation, 
should they want to do so. Indeed the evidence establishes that that was the principal motivation 
in so acting.
The conclusion that, in creating two new board positions on December 31 and electing Messrs. 
Devaney and Winters to fill those positions the board was principally motivated to prevent or delay 
the shareholders from possibly placing a majority of new members on the board, is critical to my 
analysis of the central issue posed by the first filed of the two pending cases. If the board in fact 
was not so motivated, but rather had taken action completely independently of the consent 
solicitation, which merely had an incidental impact upon the possible effectuation of any action 
authorized by the shareholders, it is very unlikely that such action would be subject to judicial 
nullification. The board, as a general matter, is under no fiduciary obligation to suspend its active 
management of the firm while the consent solicitation process goes forward.
There is testimony in the record to support the proposition that, in acting on December 31, the 
board was principally motivated simply to implement a plan to expand the Atlas board that 
preexisted the September, 1987 emergence of Blasius as an active shareholder. I have no doubt 
that the addition of Mr. Winters, an expert in mining economics, and Mr. Devaney, a financial 
expert employed by the Company, strengthened the Atlas board and, should anyone ever have 
reason to review the wisdom of those choices, they would be found to be sensible and prudent. I 
cannot conclude, however, that the strengthening of the board by the addition of these men was 
the principal motive for the December 31 action. […] [Court discusses the evidence that leads to 
this conclusion]
The timing of these events is, in my opinion, consistent only with the conclusion that Mr. Weaver 
and Mr. Masinter originated, and the board immediately endorsed, the notion of adding these 
competent, friendly individuals to the board, not because the board felt an urgent need to get them 
on the board immediately for reasons relating to the operations of Atlas' business, but because to 
do so would, for the moment, preclude a majority of shareholders from electing eight new board 
members selected by Blasius. As explained below, I conclude that, in so acting, the board was not 
selfishly motivated simply to retain power.
There was no discussion at the December 31 meeting of the feasibility or wisdom of the Blasius 
restructuring proposal. While several of the directors had an initial impression that the plan was 
not feasible and, if implemented, would likely result in the eventual liquidation of the Company, 
they had not yet focused upon and acted on that subject. Goldman Sachs had not yet made its 
report, which was scheduled to be given January 6.
The January 6 Rejection of the Blasius Proposal.
On January 6, the board convened for its scheduled meeting. At that time, it heard a full report 
from its financial advisor concerning the feasibility of the Blasius restructuring proposal. […]
After completing that presentation, Goldman Sachs concluded with its view that if Atlas 
implemented the Blasius restructuring proposal (i) a severe drain on operating cash flow would 
result, (ii) Atlas would be unable to service its long-term debt and could end up in bankruptcy, (iii) 
the common stock of Atlas would have little or no value, and (iv) since Atlas would be unable to 
generate sufficient cash to service its debt, the debentures contemplated to be issued in the 
proposed restructuring could have a value of only 20% to 30% of their face amount. Goldman 
Sachs also said that it knew of no financial restructuring that had been undertaken by a company 
where the company had no chance of repaying its debt, which, in its judgment, would be Atlas' 
situation if it implemented the Blasius restructuring proposal. Finally, Goldman Sachs noted that 
if Atlas made a meaningful commercial discovery of gold after implementation of the Blasius 
restructuring proposal, Atlas would not have the resources to develop the discovery.
The board then voted to reject the Blasius proposal. […]
[… Legal Analysis]
Plaintiff attacks the December 31 board action as a selfishly motivated effort to protect the 
incumbent board from a perceived threat to its control of Atlas. […] The December 31 action is 
also said to have been taken in a grossly negligent manner, since it was designed to preclude the 
recapitalization from being pursued, and the board had no basis at that time to make a prudent 
determination about the wisdom of that proposal, nor was there any emergency that required it to 
act in any respect regarding that proposal before putting itself in a position to do so advisedly.
Defendants, of course, contest every aspect of plaintiffs' claims. They claim the formidable 
protections of the business judgment rule. […] They say that, in creating two new board positions 
and filling them on December 31, they acted without a conflicting interest (since the Blasius 
proposal did not, in any event, challenge their places on the board), they acted with due care (since 
they well knew the persons they put on the board and did not thereby preclude later consideration 
of the recapitalization), and they acted in good faith (since they were motivated, they say, to protect 
the shareholders from the threat of having an impractical, indeed a dangerous, recapitalization 
program foisted upon them). Accordingly, defendants assert there is no basis to conclude that their 
December 31 action constituted any violation of the duty of the fidelity that a director owes by 
reason of his office to the corporation and its shareholders. […]
One of the principal thrusts of plaintiffs' argument is that, in acting to appoint two additional 
persons of their own selection, including an officer of the Company, to the board, defendants were 
motivated not by any view that Atlas' interest (or those of its shareholders) required that action, 
but rather they were motivated improperly, by selfish concern to maintain their collective control 
over the Company. That is, plaintiffs say that the evidence shows there was no policy dispute or 
issue that really motivated this action, but that asserted policy differences were pretexts for 
entrenchment for selfish reasons. If this were found to be factually true, one would not need to 
inquire further. The action taken would constitute a breach of duty.
In support of this view, plaintiffs point to the early diary entry of Mr. Weaver, to the lack of any 
consideration at all of the Blasius recapitalization proposal at the December 31 meeting, the lack 
of any substantial basis for the outside directors to have had any considered view on the subject 
by that time-not having had any view from Goldman Sachs nor seen the financial data that it 
regarded as necessary to evaluate the proposal-and upon what it urges is the grievously flawed, 
slanted analysis that Goldman Sachs finally did present.
While I am satisfied that the evidence is powerful, indeed compelling, that the board was chiefly 
motivated on December 31 to forestall or preclude the possibility that a majority of shareholders 
might place on the Atlas board eight new members sympathetic to the Blasius proposal, it is less 
clear with respect to the more subtle motivational question: whether the existing members of the 
board did so because they held a good faith belief that such shareholder action would be selfinjurious and shareholders needed to be protected from their own judgment.
On balance, I cannot conclude that the board was acting out of a self-interested motive in any 
important respect on December 31. I conclude rather that the board saw the “threat” of the Blasius 
recapitalization proposal as posing vital policy differences between itself and Blasius. It acted, I 
conclude, in a good faith effort to protect its incumbency, not selfishly, but in order to thwart 
implementation of the recapitalization that it feared, reasonably, would cause great injury to the 
Company.
The real question the case presents, to my mind, is whether, in these circumstances, the board, 
even if it is acting with subjective good faith (which will typically, if not always, be a contestable 
or debatable judicial conclusion), may validly act for the principal purpose of preventing the 
shareholders from electing a majority of new directors. […]
It is established in our law that a board may take certain steps-such as the purchase by the 
corporation of its own stock-that have the effect of defeating a threatened change in corporate 
control, when those steps are taken advisedly, in good faith pursuit of a corporate interest, and are 
reasonable in relation to a threat to legitimate corporate interests posed by the proposed change in 
control. Does this rule-that the reasonable exercise of good faith and due care generally validates, 
in equity, the exercise of legal authority even if the act has an entrenchment effect-apply to action 
designed for the primary purpose of interfering with the effectiveness of a stockholder vote? Our 
authorities, as well as sound principles, suggest that the central importance of the franchise to the 
scheme of corporate governance, requires that, in this setting, that rule not be applied and that 
closer scrutiny be accorded to such transaction.
1. Why the deferential business judgment rule does not apply to board acts taken for the primary 
purpose of interfering with a stockholder's vote, even if taken advisedly and in good faith.
A. The question of legitimacy.
The shareholder franchise is the ideological underpinning upon which the legitimacy of directorial 
power rests. Generally, shareholders have only two protections against perceived inadequate 
business performance. They may sell their stock (which, if done in sufficient numbers, may so 
affect security prices as to create an incentive for altered managerial performance), or they may 
vote to replace incumbent board members.
It has, for a long time, been conventional to dismiss the stockholder vote as a vestige or ritual of 
little practical importance. It may be that we are now witnessing the emergence of new institutional 
voices and arrangements that will make the stockholder vote a less predictable affair than it has 
been. Be that as it may, however, whether the vote is seen functionally as an unimportant 
formalism, or as an important tool of discipline, it is clear that it is critical to the theory that 
legitimates the exercise of power by some (directors and officers) over vast aggregations of 
property that they do not own. Thus, when viewed from a broad, institutional perspective, it can 
be seen that matters involving the integrity of the shareholder voting process involve consideration 
not present in any other context in which directors exercise delegated power.
B. Questions of this type raise issues of the allocation of authority as between the board and the 
shareholders.
The distinctive nature of the shareholder franchise context also appears when the matter is viewed 
from a less generalized, doctrinal point of view. From this point of view, as well, it appears that 
the ordinary considerations to which the business judgment rule originally responded are simply 
not present in the shareholder voting context. That is, a decision by the board to act for the primary 
purpose of preventing the effectiveness of a shareholder vote inevitably involves the question who, 
as between the principal and the agent, has authority with respect to a matter of internal corporate 
governance. That, of course, is true in a very specific way in this case which deals with the question 
who should constitute the board of directors of the corporation, but it will be true in every instance 
in which an incumbent board seeks to thwart a shareholder majority. A board's decision to act to 
prevent the shareholders from creating a majority of new board positions and filling them does not 
involve the exercise of the corporation's power over its property, or with respect to its rights or 
obligations; rather, it involves allocation, between shareholders as a class and the board, of 
effective power with respect to governance of the corporation. […]
2. What rule does apply: per se invalidity of corporate acts intended primarily to thwart effective 
exercise of the franchise or is there an intermediate standard?
Plaintiff argues for a rule of per se invalidity once a plaintiff has established that a board has acted 
for the primary purpose of thwarting the exercise of a shareholder vote. […]
A per se rule that would strike down, in equity, any board action taken for the primary purpose of 
interfering with the effectiveness of a corporate vote would have the advantage of relative clarity 
and predictability. It also has the advantage of most vigorously enforcing the concept of corporate 
democracy. The disadvantage it brings along is, of course, the disadvantage a per se rule always 
has: it may sweep too broadly.
In two recent cases dealing with shareholder votes, this court struck down board acts done for the 
primary purpose of impeding the exercise of stockholder voting power. In doing so, a per se rule 
was not applied. Rather, it was said that, in such a case, the board bears the heavy burden of 
demonstrating a compelling justification for such action.
In Aprahamian v. HBO & Company, the incumbent board had moved the date of the annual 
meeting on the eve of that meeting when it learned that a dissident stockholder group had or 
appeared to have in hand proxies representing a majority of the outstanding shares. The court 
restrained that action and compelled the meeting to occur as noticed, even though the board stated 
that it had good business reasons to move the meeting date forward, and that that action was 
recommended by a special committee. […]
[Discussion of the second case was omitted]
In my view, our inability to foresee now all of the future settings in which a board might, in good 
faith, paternalistically seek to thwart a shareholder vote, counsels against the adoption of a per se
rule invalidating, in equity, every board action taken for the sole or primary purpose of thwarting 
a shareholder vote, even though I recognize the transcending significance of the franchise to the 
claims to legitimacy of our scheme of corporate governance. It may be that some set of facts would 
justify such extreme action. This, however, is not such a case.
3. Defendants have demonstrated no sufficient justification for the action of December 31 which 
was intended to prevent an unaffiliated majority of shareholders from effectively exercising their 
right to elect eight new directors.
The board was not faced with a coercive action taken by a powerful shareholder against the 
interests of a distinct shareholder constituency (such as a public minority). It was presented with a 
consent solicitation by a 9% shareholder. Moreover, here it had time (and understood that it had 
time) to inform the shareholders of its views on the merits of the proposal subject to stockholder 
vote. The only justification that can, in such a situation, be offered for the action taken is that the 
board knows better than do the shareholders what is in the corporation's best interest. While that 
premise is no doubt true for any number of matters, it is irrelevant (except insofar as the 
shareholders wish to be guided by the board's recommendation) when the question is who should 
comprise the board of directors. The theory of our corporation law confers power upon directors 
as the agents of the shareholders; it does not create Platonic masters. It may be that the Blasius 
restructuring proposal was or is unrealistic and would lead to injury to the corporation and its 
shareholders if pursued. Having heard the evidence, I am inclined to think it was not a sound 
proposal. The board certainly viewed it that way, and that view, held in good faith, entitled the 
board to take certain steps to evade the risk it perceived. It could, for example, expend corporate 
funds to inform shareholders and seek to bring them to a similar point of view. But there is a vast 
difference between expending corporate funds to inform the electorate and exercising power for 
the primary purpose of foreclosing effective shareholder action. A majority of the shareholders, 
who were not dominated in any respect, could view the matter differently than did the board. If 
they do, or did, they are entitled to employ the mechanisms provided by the corporation law and 
the Atlas certificate of incorporation to advance that view. They are also entitled, in my opinion, 
to restrain their agents, the board, from acting for the principal purpose of thwarting that action.
I therefore conclude that, even finding the action taken was taken in good faith, it constituted an 
unintended violation of the duty of loyalty that the board owed to the shareholders. […]
"""

metadata = extract_metadata_text(sample_text)
print(metadata)

# Store the metadata in a JSON file
output_path = "metadata3.json"
with open(output_path, 'w', encoding='utf-8') as json_file:
    json.dump(metadata, json_file, indent=4)

print(f"Metadata has been saved to {output_path}")