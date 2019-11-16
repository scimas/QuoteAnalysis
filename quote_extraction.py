import re
import nltk
from nltk.tokenize import sent_tokenize


def find_quotes_in_text(text):
    """Returns a list of quotes from given text."""
    quotes_regex = re.compile('(?:\u201c(.*?)\u201d)')
    quotes = [q for q in quotes_regex.findall(text)]
    return quotes


def find_sentences_containing_quotes(quotes, text):
    """Returns a dictionary of quotes and sentences containing the quote."""
    sent_quote_dict = {}
    sentences = sent_tokenize(text)
    for sentence in sentences:
        for quote in quotes:
            if quote in sentence:
                sent_quote_dict[quote] = sentence
    return sent_quote_dict


def find_sentences_before_after_quotes(quotes, text):
    """Returns a dictionary of quotes and sentences before the sentence containing the quote."""
    before_sent_quote_dict = {}
    after_sent_quote_dict = {}
    sentences = sent_tokenize(text)
    for sentence in sentences:
        for quote in quotes:
            if quote in sentence:
                quote_sentence_index = sentences.index(sentence)
                before_quote_sent_idx = quote_sentence_index - 1
                after_quote_sent_idx = quote_sentence_index + 1
                if before_quote_sent_idx < 0:
                    before_sent_quote_dict[quote] = "No sentence present before quote"
                else:
                    before_sent_quote_dict[quote] = sentences[before_quote_sent_idx]
                if after_quote_sent_idx > len(sentences) - 1:
                    after_sent_quote_dict[quote] = "No sentence present after quote"
                else:
                    after_sent_quote_dict[quote] = sentences[after_quote_sent_idx]
    return before_sent_quote_dict, after_sent_quote_dict


example_text = """Senior Trump administration officials considered resigning en masse last year in a “midnight self-massacre” to sound a public alarm about President Trump’s conduct, but rejected the idea because they believed it would further destabilize an already teetering government, according to a new book by an unnamed author. In “A Warning” by Anonymous, obtained by The Washington Post ahead of its release, a writer described only as “a senior official in the Trump administration” paints a chilling portrait of the president as cruel, inept and a danger to the nation he was elected to lead. The author — who first captured attention in 2018 as the unidentified author of a New York Times opinion column — describes Trump careening from one self-inflicted crisis to the next, “like a twelve-year-old in an air traffic control tower, pushing the buttons of government indiscriminately, indifferent to the planes skidding across the runway and the flights frantically diverting away from the airport.” The book is an unsparing character study of Trump, from his morality to his intellectual depth, which the author writes is based on his or her observations and experiences. The author claims many other current and former administration officials share his or her views. The 259-page book — which was published by Twelve, an imprint of Grand Central Publishing/Hachette Book Group, and goes on sale Nov. 19 — does not re-create many specific episodes in vivid detail, which the author writes was intentional to protect his or her identity. At a moment when a stream of political appointees and career public servants have testified before Congress about Trump’s conduct as part of the House impeachment inquiry, the book’s author defends his or her decision to remain anonymous. “I have decided to publish this anonymously because this debate is not about me,” the author writes. “It is about us. It is about how we want the presidency to reflect our country, and that is where the discussion should center. Some will call this ‘cowardice.’ My feelings are not hurt by the accusation. Nor am I unprepared to attach my name to criticism of President Trump. I may do so, in due course.” White House press secretary Stephanie Grisham derided the book as a “work of fiction” and its anonymous author as a “coward.” “The coward who wrote this book didn’t put their name on it because it is nothing but lies,” Grisham wrote in an email. “Real authors reach out to their subjects to get things fact checked — but this person is in hiding, making that very basic part of being a real writer impossible. Reporters who choose to write about this farce should have the journalistic integrity to cover the book as what it is — a work of fiction.” Earlier this week, the Justice Department warned Hachette and the author’s agents, Matt Latimer and Keith Urbahn of Javelin, that the anonymous official may be violating a nondisclosure agreement. Javelin responded by accusing the administration of seeking to unmask the author. The author’s Sept. 5, 2018, op-ed in the Times, headlined “I Am Part of the Resistance Inside the Trump Administration,” depicted some senior officials as a bulwark protecting the country from the president’s reckless impulses. Trump denounced it at the time as treasonous. In the book, the author repudiates the central thesis of the column: “I was wrong about the ‘quiet resistance’ inside the Trump administration. Unelected bureaucrats and cabinet appointees were never going to steer Donald Trump the right direction in the long run, or refine his malignant management style. He is who he is.” The author describes senior officials waking up in the morning “in a full-blown panic” over the wild pronouncements the president had made on Twitter. “It’s like showing up at the nursing home at daybreak to find your elderly uncle running pantsless across the courtyard and cursing loudly about the cafeteria food, as The book depicts Trump as making misogynistic and racist comments behind the scenes. “I’ve sat and listened in uncomfortable silence as he talks about a woman’s appearance or performance,” the author writes. “He comments on makeup. He makes jokes about weight. He critiques clothing. He questions the toughness of women in and around his orbit. He uses words like ‘sweetie’ and ‘honey’ to address accomplished professionals. This is precisely the way a boss shouldn’t act in the work environment.” The author alleges that Trump attempted a Hispanic accent during an Oval Office meeting to complain about migrants crossing the U.S.-Mexico border. “We get these women coming in with like seven children,” Trump said, according to the book. “They are saying, ‘Oh, please help! My husband left me!’ They are useless. They don’t do anything for our country. At least if they came in with a husband we could put him in the fields to pick corn or something.” The author argues that Trump is incapable of leading the United States through a monumental international crisis, describing how he tunes out intelligence and national security briefings and theorizing that foreign adversaries see him as “a simplistic pushover” who is susceptible to flattery and easily manipulated. After the 2018 killing of Washington Post columnist Jamal Khashoggi by Saudi agents, the author writes, Trump vented to advisers and said he would be foolish to stand up to Saudi Crown Prince Mohammed bin Salman. “Do you know how stupid it would be to pick this fight?” Trump said, according to the book. “Oil would go up to one hundred fifty dollars a barrel. Jesus. How [expletive] stupid would I be?” The book contains a handful of startling assertions that are not backed up with evidence, such as a claim that if a majority of the Cabinet were prepared to remove Trump from office under the 25th Amendment, Vice President Pence would have been supportive. Pence denied this on Thursday, calling the book “appalling” and telling reporters, “I never heard anything in my time as vice president about the 25th Amendment. And why would I?” One theme laced throughout the book is Trump’s indifference to the boundaries of the law. The author writes that Trump considered presidential pardons as “unlimited ‘Get Out of Jail Free’ cards on a Monopoly board,” referring to news reports that he had offered pardons to aides. As he ranted about federal courts ruling against some of his policies, including the 2017 travel ban, the author writes, Trump once asked White House lawyers to draft a bill to send to Congress reducing the number of federal judges. “Can we just get rid of the judges? Let’s get rid of the [expletive] judges,” the president said, according to the book. “There shouldn’t be any at all, really.” The author portrays Trump as fearful of coups against him and suspicious of note-takers on his staff. According to the book, the president shouted at an aide who was scribbling in a notebook during a meeting, “What the [expletive] are you doing?” He added, “Are you [expletive] taking notes?” The aide apologized and closed the notebook. The author also ruminates about Trump’s fitness for office, describing him as reckless and without full control of his faculties. “I am not qualified to diagnose the president’s mental acuity,” the author writes. “All I can tell you is that normal people who spend any time with Donald Trump are uncomfortable by what they witness. He stumbles, slurs, gets confused, is easily irritated, and has trouble synthesizing information, not occasionally but with regularity. Those who would claim otherwise are lying to themselves or to the country.”"""
example_text_quotes = find_quotes_in_text(example_text)
sent_quote_dict = find_sentences_containing_quotes(example_text_quotes, example_text)
before_sent_quote_dict, after_sent_quote_dict = find_sentences_before_after_quotes(example_text_quotes, example_text)
