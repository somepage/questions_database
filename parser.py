import lxml.html
import requests
import pickle


def clear_text(s):
    return s.replace('\n', ' ').replace('\xa0', ' ').strip()


def parse_page(i):
    question = []
    answer = []
    comment = []
    sources = []
    author = []

    link = 'http://db.chgk.info/last?page=' + str(i)
    print(link, end=' ')
    response = requests.get(link)
    print(response.status_code)
    tree = lxml.html.fromstring(response.text)
    rounds = tree.xpath('//div[@id="main"]/table[@class="last_packages"]/tr[@class="odd" or "even"]/td[2]/a/@href')

    for round in rounds:
        link_round = 'http://db.chgk.info/' + str(round)
        response = requests.get(link_round)
        print(link_round, end=' ')
        print(response.status_code)
        tree = lxml.html.fromstring(response.text)
        question_buf = list(
            filter((lambda x: x != '\n    ' and x != ', ' and x != ' '),
                   tree.xpath('//div[@class="question"]/p/text()')))
        answer_buf = list(
            filter((lambda x: x != '\n    ' and x != ', ' and x != ' '),
                   tree.xpath('//div[@class="question"]/div/p[1]/text()')))
        comment_buf = list(
            filter((lambda x: x != '\n    ' and x != ', ' and x != ' '),
                   tree.xpath('//div[@class="question"]/div/p[2]/text()')))
        sources_buf = list(
            filter((lambda x: x != '\n    ' and x != ', ' and x != ' '),
                   tree.xpath('//div[@class="question"]/div/p[3]/text()')))
        author_buf = list(
            filter((lambda x: x != '\n    ' and x != ', ' and x != ' '),
                   tree.xpath('//div[@class="question"]/div/p[4]/text()')))
        question.append(list(map(clear_text, question_buf)))
        answer.append(list(map(clear_text, answer_buf)))
        comment.append(list(map(clear_text, comment_buf)))
        sources.append(list(map(clear_text, sources_buf)))
        author.append(list(map(clear_text, author_buf)))

    tuple_q = (question, answer, comment, sources, author)
    pickle.dump(tuple_q, open("dbchgk.pickle", "ab"))

    return 0
