# -*- coding: utf-8 -*-
import cgi
import logging

from question import Question
from answer import Answer
from ResponseFormatJSON import ResponseFormatJSON

#from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from django.utils import simplejson
from decimal import Decimal, ROUND_HALF_UP

# レスポンスデータフォーマット(JSON)
_ResponseFormat = ResponseFormatJSON()


class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write('<html><body>')

        questions = db.GqlQuery("SELECT * FROM Question ORDER BY date DESC LIMIT 10")
        
        for question in questions:
            if question.author:
                self.response.out.write('<b>%s</b> wrote:' % question.author)
            else:
                self.response.out.write('An anonymous person wrote:')
                self.response.out.write('<blockquote>No = %s</blockquote>' % cgi.escape(str(question.no)))
            
            self.response.out.write('<blockquote>no = %s</blockquote>' % cgi.escape(str(question.key().id())))
            self.response.out.write('<blockquote>title = %s</blockquote>' % cgi.escape(question.title))
            self.response.out.write('<blockquote>detail = %s</blockquote>' % cgi.escape(question.detail))   
            self.response.out.write('<blockquote>bakyo = %s</blockquote>' % cgi.escape(str(question.bakyo)))
            self.response.out.write('<blockquote>honba = %s</blockquote>' % cgi.escape(str(question.honba)))
            self.response.out.write('<blockquote>cha = %s</blockquote>' % cgi.escape(str(question.cha)))
            self.response.out.write('<blockquote>junme = %s</blockquote>' % cgi.escape(str(question.junme)))
            self.response.out.write('<blockquote>tenbo = %s</blockquote>' % cgi.escape(str(question.tenbo)))
            self.response.out.write('<blockquote>tehai = %s</blockquote>' % cgi.escape(str(question.tehai)))
            self.response.out.write('<blockquote>tsumo = %s</blockquote>' % cgi.escape(str(question.tsumo)))
            self.response.out.write('<blockquote>dora = %s</blockquote>' % cgi.escape(str(question.dora)))
            self.response.out.write('<blockquote>date = %s</blockquote>' % cgi.escape(str(question.date)))

        # Write the submission form and the footer of the page
        self.response.out.write("""
        <form action="/PutQuestion" method="get">
        <div>No:<textarea name="no"></textarea></div>
        <div>Author:<textarea name="author"></textarea></div>
        <div>Situation:<textarea name="situation"></textarea></div>
        <div>Tehai:<textarea name="tehai"></textarea></div>
        <div>Tsumo:<textarea name="tsumo"></textarea></div>
        <div>Dora:<textarea name="dora"></textarea></div>
        <div><input type="submit" value="Put Question"></div>
        </form>
        
        <form action="/GetQuestion" method="get">
        <div>No:<textarea name="no"></textarea></div>
        <div><input type="submit" value="Get Question"></div>
        </form>
        </body>
        </html>""")

class PutQuestion(webapp.RequestHandler):
    def get(self):
        # 本来はこうやって取る
        #instr = self.request.get('question')
        instr = '{"Title":"この状況で何を切る？？", "Detail":"起家で迎えた東一局、いきなり迷う配牌が来ました。¥n三色を狙いたいのですが、何を切れば良い？", "Bakyo":1, "Honba":1, "Cha":1, "Junme":16, "Tenbo":30000, "Tehai":[14,65,16,24,75,26,34,85,36,41,41,41,46], "Dora":[44], "Tsumo":47, "Author":"saito"}'
        in_question = simplejson.loads(instr)
        
        #for check parameter
        author = in_question['Author']
        title = in_question['Title']
        detail = in_question['Detail']
        bakyo = in_question['Bakyo']
        honba = in_question['Honba']
        cha = in_question['Cha']
        junme = in_question['Junme']
        tenbo = in_question['Tenbo']
        tehai = in_question['Tehai']
        tsumo = in_question['Tsumo']
        dora = in_question['Dora']
        logging.debug(junme)
        logging.debug(tenbo)
        logging.debug(dora)
        
        # 問題を１件追加
        question = Question()
        #question.no = int(self.request.get('no'))
        question.author = author
        question.title = title
        question.detail = detail
        question.bakyo = bakyo
        question.honba = honba
        question.cha = cha
        question.junme = junme
        question.tenbo = tenbo
        question.tehai = tehai
        question.tsumo = tsumo
        question.dora = dora
        question.put()
        
#        question = Question()
#        question.no = int(self.request.get('no'))
#        question.author = self.request.get('author')
#        question.situation = self.request.get('situation')
#        question.tehai = self.request.get('tehai')
#        question.tsumo = int(self.request.get('tsumo'))
#        question.dora = int(self.request.get('dora'))
#        question.put()

#        self.redirect('/')

        response_data = {}
        response_data['No'] = question.key().id()
        response_data['Date'] = str(question.date)
        
        # レスポンスデータ作成
        resp = _ResponseFormat.create("PutQuestion", True, response_data)
        
        # レスポンス送信
        send_response(self, resp)

class GetQuestion(webapp.RequestHandler):
    def get(self):
        
        #for check parameter
        no = int(self.request.get('no'))
        logging.debug(str(no))
        
        # 問題を１件取得
        question = Question().get_by_id(no)
        
        response_data = {}
        response_data['No'] = question.key().id()
        response_data['Date'] = str(question.date)
        response_data['Author'] = question.author
        response_data['Title'] = question.title
        response_data['Detail'] = question.detail
        response_data['Bakyo'] = question.bakyo
        response_data['Honba'] = question.honba
        response_data['Cha'] = question.cha
        response_data['Junme'] = question.junme
        response_data['Tenbo'] = question.tenbo
        response_data['Tehai'] = question.tehai
        response_data['Tsumo'] = question.tsumo
        response_data['Dora'] = question.dora
        
        # レスポンスデータ作成
        resp = _ResponseFormat.create("GetQuestion", True, response_data)
        
        # レスポンス送信
        send_response(self, resp)

class GetNewList(webapp.RequestHandler):
    def get(self):
        # 取得件数
        limit = int(self.request.get('limit'))
        # 取得開始オフセット
        offset = int(self.request.get('offset'))
        
        # 前問題を日付の降順で取得するクエリ
        query = Question().all().order('-date')
        # 件数とオフセットを指定して取得
        question_list = query.fetch(limit, offset)
        
        # レスポンス用の問題リスト作成
        question_map_list = []
        for question in question_list:
            question_map = {}
            question_map['No'] = question.key().id()
            question_map['Date'] = str(question.date)
            question_map['Author'] = question.author
            question_map['Title'] = question.title
            question_map['Detail'] = question.detail
            question_map['Bakyo'] = question.bakyo
            question_map['Honba'] = question.honba
            question_map['Cha'] = question.cha
            question_map['Junme'] = question.junme
            question_map['Tenbo'] = question.tenbo
            question_map['Tehai'] = question.tehai
            question_map['Tsumo'] = question.tsumo
            question_map['Dora'] = question.dora
            
            question_map_list.append(question_map)
        
        # レスポンスデータ(問題のリスト)
        response_data = {}    
        response_data['QuestionList'] = question_map_list
        
        # レスポンスデータ作成
        resp = _ResponseFormat.create("GetNewList", True, response_data)
        
        # レスポンス送信
        send_response(self, resp)

class PutAnswer(webapp.RequestHandler):        
    def get(self):
        #for check parameter
        no = int(self.request.get('no'))
        pai = int(self.request.get('pai'))
        logging.debug(str(no))
        
        self.increment_answer(no, pai)

#        ans_key_name = "key_" + str(no) + "_" + str(pai)
#        answer = Answer.get_or_insert(ans_key_name, question_no=no, pai=pai)
#        answer.vote_num += 1
#        answer.put()
#        logging.debug(str(answer.question_no))
#        logging.debug(str(answer.pai))
#        logging.debug(str(answer.vote_num))

        # レスポンスデータ(No)
        response_data = {}
        response_data['No'] = no
        
        # レスポンスデータ作成
        resp = _ResponseFormat.create("PutAnswer", True, response_data)
        
        # レスポンス送信
        send_response(self, resp)

    # トランザクション内でAnswerをインクリメント
    def increment_answer(self, no, pai):
        def txn():
            ans_key_name = "key_" + str(no) + "_" + str(pai)
            #answer = Answer.get_or_insert(ans_key_name, question_no=no, pai=pai)
            answer = Answer.get_by_key_name(ans_key_name)
            if answer is None:
                answer = Answer(key_name=ans_key_name, question_no=no, pai=pai)
                
            answer.vote_num += 1
            answer.put()
    
            logging.debug("increment_answer - No:%s Pai:%s Num:%s", str(answer.question_no), str(answer.pai), str(answer.vote_num))
        
        db.run_in_transaction(txn)

class GetResult(webapp.RequestHandler):        
    def get(self):
        #for check parameter
        no = int(self.request.get('no'))
        logging.debug("GetResult INPUT: No=%s", str(no))
        
        gqlQuery = Answer.gql("WHERE question_no = :1 ORDER BY vote_num DESC", no)
        answers = gqlQuery.fetch(44)    #　麻雀牌は最大44枚
        logging.debug(len(answers))
        
        sum = Decimal(0)
        for answer in answers:
            if answer.vote_num is not None: sum += answer.vote_num
        logging.debug(sum)
        
        result_list = []
        for answer in answers:
            result_map = {}
            result_map['Pai'] = answer.pai
            result_map['Num'] = answer.vote_num
            if answer.vote_num is not None: 
                result_map['Percentage'] = (float)((Decimal(answer.vote_num * 100) / sum).quantize(Decimal('.0'), rounding=ROUND_HALF_UP))
            
            
            result_list.append(result_map)
        
        # レスポンスデータ
        response_data = {}
        response_data['No'] = no
        response_data['Results'] = result_list
        
        
        # レスポンスデータ作成
        resp = _ResponseFormat.create("GetResult", True, response_data)
        
        # レスポンス送信
        send_response(self, resp)
        

class ClearQuestions(webapp.RequestHandler):        
    def get(self):
        password = self.request.get('password')
        # パスワード認証のつもり
        if password != 'AogikandOogi':
            return
        
        # Question Entityを全件削除
        clear_entity(Question)
        
        self.response.out.write('<html><body>')
        self.response.out.write('Clear OK<br>')
        self.response.out.write('</body></html>')
        
def send_response(self, resp):
    self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
    self.response.out.write(resp)

def clear_entity(model):
    try:
        q = model.all()
        while q.count():
            m = q.fetch(100)
            db.delete(m)
            q = model.all()
    except:
        return
        
class debugClass(webapp.RequestHandler):
    def get(self):
        logging.debug("debugClass Enter")
        
        resp = ResponseFormatJSON.create(True)
        ## 書き出し
        #sample = '{"@title": "みんなのPython", "author": "柴田淳", "pub": ["SoftBank Creative", "2006"]}'
        input = '{"name": "John Smith", "age": 33, "nickname": "ジョーン"}'
        #file = open("/Users/saito/Documents/Eclipse Project/workspace/MahjongNanikiru/sample.json", "w")
        dect = simplejson.loads(input)
        ## 日本語を出力するときは、ensure_ascii=Falseにすること
        str = simplejson.dumps(dect,ensure_ascii=False,sort_keys=True)
        logging.debug(str)
        
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        self.response.out.write(str)
        
        logging.debug("debugClass Leave")

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/PutQuestion', PutQuestion),
                                      ('/GetQuestion', GetQuestion),
                                      ('/GetNewList', GetNewList),
                                      ('/PutAnswer', PutAnswer),
                                      ('/GetResult', GetResult),
                                      ('/ClearQuestions', ClearQuestions),
                                      ('/debug', debugClass)],
                                     debug=True)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
