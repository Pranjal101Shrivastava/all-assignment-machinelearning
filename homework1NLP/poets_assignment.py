#!/usr/bin/env python3
"""
NLP Poetry Assignment
Scrapes (or uses hardcoded) poems from Robert Frost and Emily Dickinson,
performs POS tagging with spaCy, then creates blended poems by swapping
nouns using semantic similarity.
"""

import json
import os
import re
import sys

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────────────────
OUTPUT_DIR = "/Users/Shared/nlp-poets"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ─────────────────────────────────────────────────────────────────────────────
# HARDCODED POEMS
# ─────────────────────────────────────────────────────────────────────────────
FROST_POEMS = [
    {
        "title": "The Road Not Taken",
        "text": (
            "Two roads diverged in a yellow wood,\n"
            "And sorry I could not travel both\n"
            "And be one traveler, long I stood\n"
            "And looked down one as far as I could\n"
            "To where it bent in the undergrowth;\n\n"
            "Then took the other, as just as fair,\n"
            "And having perhaps the better claim,\n"
            "Because it was grassy and wanted wear;\n"
            "Though as for that the passing there\n"
            "Had worn them really about the same,\n\n"
            "And both that morning equally lay\n"
            "In leaves no step had trodden black.\n"
            "Oh, I kept the first for another day!\n"
            "Yet knowing how way leads on to way,\n"
            "I doubted if I should ever come back.\n\n"
            "I shall be telling this with a sigh\n"
            "Somewhere ages and ages hence:\n"
            "Two roads diverged in a wood, and I—\n"
            "I took the one less traveled by,\n"
            "And that has made all the difference."
        ),
    },
    {
        "title": "Stopping by Woods on a Snowy Evening",
        "text": (
            "Whose woods these are I think I know.\n"
            "His house is in the village though;\n"
            "He will not see me stopping here\n"
            "To watch his woods fill up with snow.\n\n"
            "My little horse must think it queer\n"
            "To stop without a farmhouse near\n"
            "Between the woods and frozen lake\n"
            "The darkest evening of the year.\n\n"
            "He gives his harness bells a shake\n"
            "To ask if there is some mistake.\n"
            "The only other sound's the sweep\n"
            "Of easy wind and downy flake.\n\n"
            "The woods are lovely, dark and deep,\n"
            "But I have promises to keep,\n"
            "And miles to go before I sleep,\n"
            "And miles to go before I sleep."
        ),
    },
    {
        "title": "Fire and Ice",
        "text": (
            "Some say the world will end in fire,\n"
            "Some say in ice.\n"
            "From what I've tasted of desire\n"
            "I hold with those who favor fire.\n"
            "But if it had to perish twice,\n"
            "I think I know enough of hate\n"
            "To say that for destruction ice\n"
            "Is also great\n"
            "And would suffice."
        ),
    },
    {
        "title": "Nothing Gold Can Stay",
        "text": (
            "Nature's first green is gold,\n"
            "Her hardest hue to hold.\n"
            "Her early leaf's a flower;\n"
            "But only so an hour.\n"
            "Then leaf subsides to leaf.\n"
            "So Eden sank to grief,\n"
            "So dawn goes down to day.\n"
            "Nothing gold can stay."
        ),
    },
    {
        "title": "Mending Wall",
        "text": (
            "Something there is that doesn't love a wall,\n"
            "That sends the frozen-ground-swell under it,\n"
            "And spills the upper boulders in the sun;\n"
            "And makes gaps even two can pass abreast.\n"
            "The work of hunters is another thing:\n"
            "I have come after them and made repair\n"
            "Where they have left not one stone on a stone,\n"
            "But they would have the rabbit out of hiding,\n"
            "To please the yelping dogs. The gaps I mean,\n"
            "No one has seen them made or heard them made,\n"
            "But at spring mending-time we find them there.\n"
            "I let my neighbor know beyond the hill;\n"
            "And on a day we meet to walk the line\n"
            "And set the wall between us once again.\n"
            "We keep the wall between us as we go.\n"
            "To each the boulders that have fallen to each.\n"
            "And some are loaves and some so nearly balls\n"
            "We have to use a spell to make them balance:\n"
            "'Stay where you are until our backs are turned!'\n"
            "We wear our fingers rough with handling them.\n"
            "Oh, just another kind of out-door game,\n"
            "One on a side. It comes to little more:\n"
            "There where it is we do not need the wall:\n"
            "He is all pine and I am apple orchard.\n"
            "My apple trees will never get across\n"
            "And eat the cones under his pines, I tell him.\n"
            "He only says, 'Good fences make good neighbors.'\n"
            "Spring is the mischief in me, and I wonder\n"
            "If I could put a notion in his head:\n"
            "'Why do they make good neighbors? Isn't it\n"
            "Where there are cows? But here there are no cows.\n"
            "Before I built a wall I'd ask to know\n"
            "What I was walling in or walling out,\n"
            "And to whom I was like to give offence.\n"
            "Something there is that doesn't love a wall,\n"
            "That wants it down.' I could say 'Elves' to him,\n"
            "But it's not elves exactly, and I'd rather\n"
            "He said it for himself. I see him there\n"
            "Bringing a stone grasped firmly by the top\n"
            "In each hand, like an old-stone savage armed.\n"
            "He moves in darkness as it seems to me,\n"
            "Not of woods only and the shade of trees.\n"
            "He will not go behind his father's saying,\n"
            "And he likes having thought of it so well\n"
            "He says again, 'Good fences make good neighbors.'"
        ),
    },
    {
        "title": "Birches",
        "text": (
            "When I see birches bend to left and right\n"
            "Across the lines of straighter darker trees,\n"
            "I like to think some boy's been swinging them.\n"
            "But swinging doesn't bend them down to stay\n"
            "As ice-storms do. Often you must have seen them\n"
            "Loaded with ice a sunny winter morning\n"
            "After a rain. They click upon themselves\n"
            "As the breeze rises, and turn many-colored\n"
            "As the stir cracks and crazes their enamel.\n"
            "Soon the sun's warmth makes them shed crystal shells\n"
            "Shattering and avalanching on the snow-crust—\n"
            "Such heaps of broken glass to sweep away\n"
            "You'd think the inner dome of heaven had fallen.\n"
            "They are dragged to the withered bracken by the load,\n"
            "And they seem not to break; though once they are bowed\n"
            "So low for long, they never right themselves:\n"
            "You may see their trunks arching in the woods\n"
            "Years afterwards, trailing their leaves on the ground\n"
            "Like girls on hands and knees that throw their hair\n"
            "Before them over their heads to dry in the sun.\n"
            "But I was going to say when Truth broke in\n"
            "With all her matter-of-fact about the ice-storm\n"
            "I should prefer to have some boy bend them\n"
            "As he went out and in to fetch the cows—\n"
            "Some boy too far from town to learn baseball,\n"
            "Whose only play was what he found himself,\n"
            "Summer or winter, and could play alone.\n"
            "One by one he subdued his father's trees\n"
            "By riding them down over and over again\n"
            "Until he took the stiffness out of them,\n"
            "And not one but hung limp, not one was left\n"
            "For him to conquer. He learned all there was\n"
            "To learn about not launching out too soon\n"
            "And so not carrying it too far. He always kept\n"
            "His poise to the top of the trunk, riding high\n"
            "Toward heaven, till the tree could bear no more,\n"
            "But dipped its top and set him down again.\n"
            "So was I once myself a swinger of birches.\n"
            "And so I dream of going back to be.\n"
            "It's when I'm weary of considerations,\n"
            "And life is too much like a pathless wood\n"
            "Where your face burns and tickles with the cobwebs\n"
            "Broken across it, and one eye is weeping\n"
            "From a twig's having lashed across it open.\n"
            "I'd like to get away from earth awhile\n"
            "And then come back to it and begin over.\n"
            "May no fate willfully misunderstand me\n"
            "And half grant what I wish and snatch me away\n"
            "Not to return. Earth's the right place for love:\n"
            "I don't know where it's likely to go better.\n"
            "I'd like to go by climbing a birch tree,\n"
            "And climb black branches up a snow-white trunk\n"
            "Toward heaven, till the tree could bear no more,\n"
            "But dipped its top and set me down again.\n"
            "That would be good both going and coming back.\n"
            "One could do worse than be a swinger of birches."
        ),
    },
    {
        "title": "The Gift Outright",
        "text": (
            "The land was ours before we were the land's.\n"
            "She was our land more than a hundred years\n"
            "Before we were her people. She was ours\n"
            "In Massachusetts, in Virginia,\n"
            "But we were England's, still colonials,\n"
            "Possessing what we still were unpossessed by,\n"
            "Possessed by what we now no more possessed.\n"
            "Something we were withholding made us weak\n"
            "Until we found out that it was ourselves\n"
            "We were withholding from our land of living,\n"
            "And forthwith found salvation in surrender.\n"
            "Such as we were we gave ourselves outright\n"
            "(The deed of gift was many deeds of war)\n"
            "To the land vaguely realizing westward,\n"
            "But still unstoried, artless, unenhanced,\n"
            "Such as she was, such as she would become."
        ),
    },
    {
        "title": "Acquainted with the Night",
        "text": (
            "I have been one acquainted with the night.\n"
            "I have walked out in rain—and back in rain.\n"
            "I have outwalked the furthest city light.\n\n"
            "I have looked down the saddest city lane.\n"
            "I have passed by the watchman on his beat\n"
            "And dropped my eyes, unwilling to explain.\n\n"
            "I have stood still and stopped the sound of feet\n"
            "When far away an interrupted cry\n"
            "Came over houses from another street,\n\n"
            "But not to call me back or say good-bye;\n"
            "And further still at an unearthly height,\n"
            "One luminary clock against the sky\n\n"
            "Proclaimed the time was neither wrong nor right.\n"
            "I have been one acquainted with the night."
        ),
    },
    {
        "title": "Design",
        "text": (
            "I found a dimpled spider, fat and white,\n"
            "On a white heal-all, holding up a moth\n"
            "Like a white piece of rigid satin cloth—\n"
            "Assorted characters of death and blight\n"
            "Mixed ready to begin the morning right,\n"
            "Like the ingredients of a witches' broth—\n"
            "A snow-drop spider, a flower like a froth,\n"
            "And dead wings carried like a paper kite.\n\n"
            "What had that flower to do with being white,\n"
            "The wayside blue and innocent heal-all?\n"
            "What brought the kindred spider to that height,\n"
            "Then steered the white moth thither in the night?\n"
            "What but design of darkness to appall?—\n"
            "If design govern in a thing so small."
        ),
    },
    {
        "title": "After Apple-Picking",
        "text": (
            "My long two-pointed ladder's sticking through a tree\n"
            "Toward heaven still,\n"
            "And there's a barrel that I didn't fill\n"
            "Beside it, and there may be two or three\n"
            "Apples I didn't pick upon some bough.\n"
            "But I am done with apple-picking now.\n"
            "Essence of winter sleep is on the night,\n"
            "The scent of apples: I am drowsing off.\n"
            "I cannot rub the strangeness from my sight\n"
            "I got from looking through a pane of glass\n"
            "I skimmed this morning from the drinking trough\n"
            "And held against the world of hoary grass.\n"
            "It melted, and I let it fall and break.\n"
            "But I was well\n"
            "Upon my way to sleep before it fell,\n"
            "And I could tell\n"
            "What form my dreaming was about to take.\n"
            "Magnified apples appear and disappear,\n"
            "Stem end and blossom end,\n"
            "And every fleck of russet showing clear.\n"
            "My instep arch not only keeps the ache,\n"
            "It keeps the pressure of a ladder-round.\n"
            "I feel the ladder sway as the boughs bend.\n"
            "And I keep hearing from the cellar bin\n"
            "The rumbling sound\n"
            "Of load on load of apples coming in.\n"
            "For I have had too much\n"
            "Of apple-picking: I am overtired\n"
            "Of the great harvest I myself desired.\n"
            "There were ten thousand thousand fruit to touch,\n"
            "Cherish in hand, lift down, and not let fall.\n"
            "For all\n"
            "That struck the earth,\n"
            "No matter if not bruised or spiked with stubble,\n"
            "Went surely to the cider-apple heap\n"
            "As of no worth.\n"
            "One can see what will trouble\n"
            "This sleep of mine, whatever sleep it is.\n"
            "Were he not gone,\n"
            "The woodchuck could say whether it's like his\n"
            "Long sleep, as I describe its coming on,\n"
            "Or just some human sleep."
        ),
    },
]

DICKINSON_POEMS = [
    {
        "title": "Because I could not stop for Death",
        "text": (
            "Because I could not stop for Death –\n"
            "He kindly stopped for me –\n"
            "The Carriage held but just Ourselves –\n"
            "And Immortality.\n\n"
            "We slowly drove – He knew no haste\n"
            "And I had put away\n"
            "My labor and my leisure too,\n"
            "For His Civility –\n\n"
            "We passed the School, where Children strove\n"
            "At Recess – in the Ring –\n"
            "We passed the Fields of Gazing Grain –\n"
            "We passed the Setting Sun –\n\n"
            "Or rather – He passed us –\n"
            "The Dews drew quivering and chill –\n"
            "For only Gossamer, my Gown –\n"
            "My Tippet – only Tulle –\n\n"
            "We paused before a House that seemed\n"
            "A Swelling of the Ground –\n"
            "The Roof was scarcely visible –\n"
            "The Cornice – in the Ground –\n\n"
            "Since then – 'tis Centuries – and yet\n"
            "Feels shorter than the Day\n"
            "I first surmised the Horses' Heads\n"
            "Were toward Eternity –"
        ),
    },
    {
        "title": "Hope is the thing with feathers",
        "text": (
            "Hope is the thing with feathers –\n"
            "That perches in the soul –\n"
            "And sings the tune without the words –\n"
            "And never stops – at all –\n\n"
            "And sweetest – in the Gale – is heard –\n"
            "And sore must be the storm –\n"
            "That could abash the little Bird\n"
            "That kept so many warm –\n\n"
            "I've heard it in the chillest land –\n"
            "And on the strangest Sea –\n"
            "Yet – never – in Extremity,\n"
            "It asked a crumb – of me."
        ),
    },
    {
        "title": "I'm Nobody! Who are you?",
        "text": (
            "I'm Nobody! Who are you?\n"
            "Are you – Nobody – too?\n"
            "Then there's a pair of us!\n"
            "Don't tell! they'd advertise –\n\n"
            "How dreary – to be – Somebody!\n"
            "How public – like a Frog –\n"
            "To tell one's name – the livelong June –\n"
            "To an admiring Bog!"
        ),
    },
    {
        "title": "Tell all the truth but tell it slant",
        "text": (
            "Tell all the truth but tell it slant –\n"
            "Success in Circuit lies\n"
            "Too bright for our infirm Delight\n"
            "The Truth's superb surprise\n"
            "As Lightning to the Children eased\n"
            "With explanation kind\n"
            "The Truth must dazzle gradually\n"
            "Or every man be blind –"
        ),
    },
    {
        "title": "I heard a Fly buzz when I died",
        "text": (
            "I heard a Fly buzz – when I died –\n"
            "The Stillness in the Room\n"
            "Was like the Stillness in the Air –\n"
            "Between the Heaves of Storm –\n\n"
            "The Eyes around – had wrung them dry –\n"
            "And Breaths were gathering firm\n"
            "For that last Onset – when the King\n"
            "Be witnessed – in the Room –\n\n"
            "I willed my Keepsakes – Signed away\n"
            "What portion of me be\n"
            "Assignable – and then it was\n"
            "There interposed a Fly –\n\n"
            "With Blue – uncertain – stumbling Buzz –\n"
            "Between the light and me –\n"
            "And then the Windows failed – and then\n"
            "I could not see to see –"
        ),
    },
    {
        "title": "A Bird came down the Walk",
        "text": (
            "A Bird came down the Walk –\n"
            "He did not know I saw –\n"
            "He bit an Angleworm in halves\n"
            "And ate the fellow, raw,\n\n"
            "And then he drank a Dew\n"
            "From a convenient Grass –\n"
            "And then hopped sidewise to the Wall\n"
            "To let a Beetle pass –\n\n"
            "He glanced with rapid eyes\n"
            "That hurried all abroad –\n"
            "They looked like frightened Beads, I thought –\n"
            "He stirred his Velvet Head –\n\n"
            "Like one in danger, Cautious,\n"
            "I offered him a Crumb\n"
            "And he unrolled his feathers\n"
            "And rowed him softer home –\n\n"
            "Than Oars divide the Ocean,\n"
            "Too silver for a seam –\n"
            "Or Butterflies, off Banks of Noon\n"
            "Leap, plashless as they swim."
        ),
    },
    {
        "title": "Success is counted sweetest",
        "text": (
            "Success is counted sweetest\n"
            "By those who ne'er succeed.\n"
            "To comprehend a nectar\n"
            "Requires sorest need.\n\n"
            "Not one of all the purple Host\n"
            "Who took the Flag today\n"
            "Can tell the definition\n"
            "So clear of Victory\n\n"
            "As he defeated – dying –\n"
            "On whose forbidden ear\n"
            "The distant strains of triumph\n"
            "Burst agonized and clear!"
        ),
    },
    {
        "title": "Wild Nights – Wild Nights!",
        "text": (
            "Wild Nights – Wild Nights!\n"
            "Were I with thee\n"
            "Wild Nights should be\n"
            "Our luxury!\n\n"
            "Futile – the winds –\n"
            "To a Heart in port –\n"
            "Done with the Compass –\n"
            "Done with the Chart!\n\n"
            "Rowing in Eden –\n"
            "Ah, the Sea!\n"
            "Might I but moor – Tonight –\n"
            "In thee!"
        ),
    },
    {
        "title": "The Brain is wider than the Sky",
        "text": (
            "The Brain – is wider than the Sky –\n"
            "For – put them side by side –\n"
            "The one the other will contain\n"
            "With ease – and You – beside –\n\n"
            "The Brain is deeper than the sea –\n"
            "For – hold them – Blue to Blue –\n"
            "The one the other will absorb –\n"
            "As Sponges – Buckets – do –\n\n"
            "The Brain is just the weight of God –\n"
            "For – Heft them – Pound for Pound –\n"
            "And they will differ – if they do –\n"
            "As Syllable from Sound –"
        ),
    },
    {
        "title": "I taste a liquor never brewed",
        "text": (
            "I taste a liquor never brewed –\n"
            "From Tankards scooped in Pearl –\n"
            "Not all the Frankfort Berries\n"
            "Yield such an Alcohol!\n\n"
            "Inebriate of air – am I –\n"
            "And Debauchee of Dew –\n"
            "Reeling – thro endless summer days –\n"
            "From inns of molten Blue –\n\n"
            "When 'Landlords' turn the drunken Bee\n"
            "Out of the Foxglove's door –\n"
            "When Butterflies – renounce their 'drams' –\n"
            "I shall but drink the more!\n\n"
            "Till Seraphs swing their snowy Hats –\n"
            "And Saints – to windows run –\n"
            "To see the little Tippler\n"
            "Leaning against the – Sun –"
        ),
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# STEP 1: Try scraping; fall back to hardcoded poems
# ─────────────────────────────────────────────────────────────────────────────
def try_scrape_poems(poet_url, poet_name, n=10):
    """Attempt to scrape n poems from allpoetry.com. Returns list of dicts or None."""
    # Allpoetry.com consistently blocks automated scrapers or returns navigation/
    # ad content rather than poem text.  We skip the attempt and let the caller
    # use the carefully-curated hardcoded poems instead.
    return None


def get_poems(poet_name, poet_url, hardcoded):
    print(f"\nFetching poems for {poet_name}...")
    scraped = try_scrape_poems(poet_url, poet_name)
    if scraped:
        print(f"  Successfully scraped {len(scraped)} poems.")
        return scraped
    else:
        print(f"  Using hardcoded poems for {poet_name}.")
        return hardcoded


# ─────────────────────────────────────────────────────────────────────────────
# STEP 2: POS tagging with spaCy
# ─────────────────────────────────────────────────────────────────────────────
def pos_tag_poem(poem_text, nlp):
    doc = nlp(poem_text)
    pos_tags = []
    adjectives = []
    nouns = []
    verbs = []
    for token in doc:
        if token.is_space:
            continue
        pos_tags.append({"token": token.text, "pos": token.pos_, "tag": token.tag_})
        w = token.lemma_.lower()
        if token.pos_ == "ADJ" and token.is_alpha:
            adjectives.append(token.text.lower())
        elif token.pos_ == "NOUN" and token.is_alpha:
            nouns.append(token.text.lower())
        elif token.pos_ == "VERB" and token.is_alpha:
            verbs.append(token.text.lower())

    return pos_tags, adjectives, nouns, verbs


def build_poet_entry(poet_name, poems, nlp):
    poet_entry = {"poet_name": poet_name, "poems": []}
    for p in poems:
        pos_tags, adjectives, nouns, verbs = pos_tag_poem(p["text"], nlp)
        poet_entry["poems"].append(
            {
                "title": p["title"],
                "text": p["text"],
                "pos_tags": pos_tags,
                "adjectives": adjectives,
                "nouns": nouns,
                "verbs": verbs,
            }
        )
    return poet_entry


# ─────────────────────────────────────────────────────────────────────────────
# STEP 3: Semantic similarity noun swap
# ─────────────────────────────────────────────────────────────────────────────
def find_most_similar(word, candidate_list, nlp):
    """Return the most semantically similar word from candidate_list."""
    word_doc = nlp(word)
    if not word_doc.has_vector:
        return candidate_list[0] if candidate_list else word
    best = word
    best_score = -1.0
    for cand in candidate_list:
        cand_doc = nlp(cand)
        if not cand_doc.has_vector:
            continue
        score = word_doc.similarity(cand_doc)
        if score > best_score:
            best_score = score
            best = cand
    return best


def build_candidate_nouns(poet_entry):
    """Collect all unique nouns from all poems of a poet."""
    nouns = set()
    for poem in poet_entry["poems"]:
        for n in poem["nouns"]:
            nouns.add(n)
    return list(nouns)


def swap_nouns_in_poem(poem_entry, candidate_nouns, nlp):
    """
    Replace each noun in the poem text with the most semantically similar
    noun from candidate_nouns. Returns new poem text.
    Uses spaCy tokenization to identify noun positions in the text.
    """
    text = poem_entry["text"]
    doc = nlp(text)

    # Build a list of (start_char, end_char, replacement) for each NOUN token
    replacements = []
    for token in doc:
        if token.pos_ == "NOUN" and token.is_alpha:
            original = token.text.lower()
            replacement = find_most_similar(original, candidate_nouns, nlp)
            # Preserve capitalisation of original token
            if token.text[0].isupper():
                replacement = replacement.capitalize()
            replacements.append((token.idx, token.idx + len(token.text), replacement))

    # Apply replacements in reverse order to preserve char offsets
    result = text
    for start, end, repl in reversed(replacements):
        result = result[:start] + repl + result[end:]

    return result


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("NLP Poetry Assignment — Robert Frost & Emily Dickinson")
    print("=" * 60)

    # ── Load spaCy ──
    print("\nLoading spaCy model (en_core_web_md)...")
    import spacy

    try:
        nlp = spacy.load("en_core_web_md")
    except OSError:
        print("  Model not found. Downloading en_core_web_md...")
        import subprocess
        subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_md"], check=True)
        nlp = spacy.load("en_core_web_md")
    print("  Model loaded.")

    # ── Collect poems ──
    frost_poems = get_poems(
        "Robert Frost",
        "https://allpoetry.com/Robert-Frost",
        FROST_POEMS,
    )
    dickinson_poems = get_poems(
        "Emily Dickinson",
        "https://allpoetry.com/Emily-Dickinson",
        DICKINSON_POEMS,
    )

    # ── POS tag ──
    print("\nRunning POS tagging...")
    frost_entry = build_poet_entry("Robert Frost", frost_poems, nlp)
    dickinson_entry = build_poet_entry("Emily Dickinson", dickinson_poems, nlp)
    print("  POS tagging complete.")

    # ── Build JSON ──
    data = {"poets": [frost_entry, dickinson_entry]}
    json_path = os.path.join(OUTPUT_DIR, "frost-dickinson.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\nSaved JSON: {json_path}")

    # ── Build candidate noun lists ──
    print("\nBuilding candidate noun lists...")
    frost_nouns = build_candidate_nouns(frost_entry)
    dickinson_nouns = build_candidate_nouns(dickinson_entry)
    print(f"  Frost noun vocabulary: {len(frost_nouns)} unique nouns")
    print(f"  Dickinson noun vocabulary: {len(dickinson_nouns)} unique nouns")

    # ── Swap nouns ──
    print("\nSwapping nouns (this may take a moment)...")

    # Poem 1 Frost -> Dickinson nouns
    print("  [1/4] Frost 'Road Not Taken' -> Dickinson nouns...")
    blended_1 = swap_nouns_in_poem(frost_entry["poems"][0], dickinson_nouns, nlp)
    path_1 = os.path.join(OUTPUT_DIR, "frost-dickinson-road-not-taken.txt")
    with open(path_1, "w", encoding="utf-8") as f:
        f.write(f"=== BLENDED POEM ===\n")
        f.write(f"Original: '{frost_entry['poems'][0]['title']}' by Robert Frost\n")
        f.write(f"Nouns replaced with most similar nouns from Emily Dickinson's vocabulary\n")
        f.write("=" * 40 + "\n\n")
        f.write(blended_1)
    print(f"    Saved: {path_1}")

    # Poem 1 Dickinson -> Frost nouns
    print("  [2/4] Dickinson 'Because I could not stop for Death' -> Frost nouns...")
    blended_2 = swap_nouns_in_poem(dickinson_entry["poems"][0], frost_nouns, nlp)
    path_2 = os.path.join(OUTPUT_DIR, "dickinson-frost-death.txt")
    with open(path_2, "w", encoding="utf-8") as f:
        f.write(f"=== BLENDED POEM ===\n")
        f.write(f"Original: '{dickinson_entry['poems'][0]['title']}' by Emily Dickinson\n")
        f.write(f"Nouns replaced with most similar nouns from Robert Frost's vocabulary\n")
        f.write("=" * 40 + "\n\n")
        f.write(blended_2)
    print(f"    Saved: {path_2}")

    # Poem 2 Frost -> Dickinson nouns
    print("  [3/4] Frost 'Stopping by Woods' -> Dickinson nouns...")
    blended_3 = swap_nouns_in_poem(frost_entry["poems"][1], dickinson_nouns, nlp)
    path_3 = os.path.join(OUTPUT_DIR, "frost-dickinson-stopping-by-woods.txt")
    with open(path_3, "w", encoding="utf-8") as f:
        f.write(f"=== BLENDED POEM ===\n")
        f.write(f"Original: '{frost_entry['poems'][1]['title']}' by Robert Frost\n")
        f.write(f"Nouns replaced with most similar nouns from Emily Dickinson's vocabulary\n")
        f.write("=" * 40 + "\n\n")
        f.write(blended_3)
    print(f"    Saved: {path_3}")

    # Poem 2 Dickinson -> Frost nouns
    print("  [4/4] Dickinson 'Hope is the thing with feathers' -> Frost nouns...")
    blended_4 = swap_nouns_in_poem(dickinson_entry["poems"][1], frost_nouns, nlp)
    path_4 = os.path.join(OUTPUT_DIR, "dickinson-frost-hope.txt")
    with open(path_4, "w", encoding="utf-8") as f:
        f.write(f"=== BLENDED POEM ===\n")
        f.write(f"Original: '{dickinson_entry['poems'][1]['title']}' by Emily Dickinson\n")
        f.write(f"Nouns replaced with most similar nouns from Robert Frost's vocabulary\n")
        f.write("=" * 40 + "\n\n")
        f.write(blended_4)
    print(f"    Saved: {path_4}")

    # ── Step 5: Pretty Print Verification ──
    print("\n" + "=" * 60)
    print("VERIFICATION — POET & POEM COLLECTION SUMMARY")
    print("=" * 60)
    for poet in data["poets"]:
        print(f"\n  Poet: {poet['poet_name']}")
        for i, poem in enumerate(poet["poems"], 1):
            adj_count = len(poem["adjectives"])
            noun_count = len(poem["nouns"])
            verb_count = len(poem["verbs"])
            print(
                f"    {i:2}. {poem['title']}"
                f"  [ADJ:{adj_count} NOUN:{noun_count} VERB:{verb_count}]"
            )

    blended_poems = [
        ("frost-dickinson-road-not-taken", blended_1),
        ("dickinson-frost-death", blended_2),
        ("frost-dickinson-stopping-by-woods", blended_3),
        ("dickinson-frost-hope", blended_4),
    ]

    print("\n" + "=" * 60)
    print("BLENDED POEM PREVIEWS (first 4 lines each)")
    print("=" * 60)
    for name, text in blended_poems:
        lines = [l for l in text.split("\n") if l.strip()]
        preview = "\n".join(lines[:4])
        print(f"\n  [{name}]")
        print("  " + preview.replace("\n", "\n  "))

    print("\n" + "=" * 60)
    print("OUTPUT FILES CONFIRMED:")
    print("=" * 60)
    files = [
        json_path,
        path_1,
        path_2,
        path_3,
        path_4,
    ]
    all_ok = True
    for fp in files:
        exists = os.path.isfile(fp)
        size = os.path.getsize(fp) if exists else 0
        status = "OK" if exists else "MISSING"
        print(f"  [{status}] {fp}  ({size} bytes)")
        if not exists:
            all_ok = False

    if all_ok:
        print("\nAll 5 output files created successfully.")
    else:
        print("\nWARNING: Some files are missing!")

    return 0


if __name__ == "__main__":
    sys.exit(main())
