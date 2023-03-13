from random import shuffle, choice, randint

from defines import MONTHS


MONTHS_i = list(MONTHS.values())
MONTHS_r = list(MONTHS.keys())


async def get_variants(correct_answer: str, n: int, correct: str, incorrect: str):
    answers = [correct_answer]
    callback = [correct]
    for index in range(n-1):
        for _ in range(10):
            incorrect_answer = generate_incorrect_answer(correct_answer)
            if incorrect_answer not in answers:
                answers.append(incorrect_answer)
                break
        callback.append(incorrect)
    variants = list(zip(answers, callback))
    shuffle(variants)
    answers, callbacks = zip(*variants)
    return list(answers), list(callbacks)


def generate_incorrect_answer(correct_answer):
    correct_answer = correct_answer.split(" ")
    false_answer = []
    for part in correct_answer:
        st = []
        for i, word in enumerate(part.split("-")):
            if word in MONTHS_i:
                new_month = [j for j in MONTHS_i if j != word]
                new_month = choice(new_month)
                st.append(new_month)
            elif word in MONTHS_r:
                new_month = [j for j in MONTHS_r if j != word]
                new_month = choice(new_month)
                st.append(new_month)
            elif word.isdigit():
                digit = int(word)
                if digit > 31:
                    shift = randint(-10, 10)
                    if shift == 0:
                        shift -= 1
                    digit += shift
                    st.append(str(digit))
                else:
                    shift = randint(2, 2)
                    digit += shift
                    digit = max(1, min(digit, 31))
                    st.append(str(digit))
            else:
                st.append(word)
        false_answer.append(range_to_string(st))

    return " ".join(false_answer)


def range_to_string(rng):
    if len(rng) == 1:
        return rng[0]

    fst = rng[0]
    snd = rng[1]
    if fst.isdigit() and snd.isdigit():
        fst, snd = int(fst), int(snd)
        if fst > snd:
            rng[0] = str(snd)
            rng[1] = str(fst)
        return "-".join(rng)

    if fst in MONTHS_i and snd in MONTHS_i:
        mth1_ind = MONTHS_i.index(fst)
        mth2_ind = MONTHS_i.index(snd)
        if mth1_ind > mth2_ind:
            rng[0] = str(snd)
            rng[1] = str(fst)
    elif fst in MONTHS_r and snd in MONTHS_r:
        mth1_ind = MONTHS_r.index(fst)
        mth2_ind = MONTHS_r.index(snd)
        if mth1_ind > mth2_ind:
            rng[0] = str(snd)
            rng[1] = str(fst)
    return "-".join(rng)
