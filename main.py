import json
import random 
import time

class Taikhoan:
    def __init__(self, username, password, name, admin = False, verified = False):
        self.username  = username
        self.password = password
        self.name = name
        self.admin = admin
        self.verified = verified

class Cauhoi:
    def __init__(self, ID, question, answer, rightanswer, level):
        self.ID = ID
        self.question = question
        self.answer = answer
        self.rightanswer = rightanswer
        self.level = level
    def In_cauhoi_admin(self):
        print("ID của câu hỏi:",self.ID)
        print("Câu hỏi:",self.question)
        print("A.",self.answer[0])
        print("B.",self.answer[1])
        print("C.",self.answer[2])
        print("D.",self.answer[3])
        print("Đáp án đúng:",self.rightanswer)
        print("Độ khó:",self.level)
    def In_cauhoi_stu(self):
        print("Câu hỏi:",self.question)
        print("A.",self.answer[0])
        print("B.",self.answer[1])
        print("C.",self.answer[2])
        print("D.",self.answer[3])
    def In_cauhoi_vaotxt(self, path_file_txt, n):
        with open(path_file_txt, "a", encoding="utf-8") as f:
            print("Câu hỏi số",n,": ",self.question,file = f)
            print("A.",self.answer[0],file = f)
            print("B.",self.answer[1],file = f)
            print("C.",self.answer[2],file = f)
            print("D.",self.answer[3],file = f)
            print("",file = f)
def Xoa_khoangtrang(string): # hàm xóa các khoảng trắng và trả về string
    string1=""
    for i in string:
        if i == " ":
            continue
        else:
            string1+=i
    return string1 
def dem_so_dong(f):
    f.seek(0)
    return sum(1 for line in f)

def Dang_ky(path_file_user): # f là file các người dùng
    with open(path_file_user,"r",encoding="utf-8") as f :
        data_user = json.load(f)
    so_luong = len(data_user)
    while True:
        username = input("Nhập tài khoản: ")
        username = Xoa_khoangtrang(username)
        password = input("Nhập mật khẩu: ")
        repassword = input("Nhập lại mật khẩu: ")
        name = input("Nhập tên của bạn: ")
        for i in range(so_luong):
            if data_user[i]["username"] == username:
                print("Đã có tài khoản này vui lòng nhập lại.")
                break
        else:
            if password != repassword:
                print("Mật khẩu không trùng khớp vui lòng nhập lại.")
            else:
                nguoi_moi = Taikhoan(username, password, name)
                new_data_user = {
                    "username":nguoi_moi.username,
                    "password":nguoi_moi.password,
                    "name": nguoi_moi.name,
                    "admin":nguoi_moi.admin,
                    "verified": nguoi_moi.verified
                }
                data_user.append(new_data_user)
                with open(path_file_user,"w",encoding="utf-8") as f:
                      json.dump(data_user, f, ensure_ascii=False)
                print("Đã gửi đăng ký thành công. Vui lòng chờ quản trị phê duyệt")
                f.close()
                break

def Phe_duyet(path_file_user):
    with open(path_file_user,"r",encoding="utf-8") as f :
        data_user = json.load(f)
    print("Các tài khoản chưa được phê duyệt là: ")
    count = 0
    lst_index = []
    index = 0
    for i in data_user:
        if i["verified"] == False:
            count +=1
            print("Người thứ",count,"với account: "+i["username"]+" Họ và tên: "+i["name"])
            lst_index.append(index)
        index+=1
    if count == 0:
        print("Không có tài khoản nào yêu cầu xác thực.")
        return
    else:
        tmp = input("Nhập các người mà bạn muốn xác thực( Cách nhau bởi khoảng trắng): ")
        lst = tmp.split() # Hàm split dùng để tách string sang list với step mong muốn mặc định là khoảng trắng
        count = 1
        for i in lst:
            if  (not i.isdigit()) or (int(i)> len(lst_index)): #isdigit trả về True nếu số là số nguyên không âm
                print("Số bạn nhập đã không hợp lệ vui lòng thử lại sau.")
                return
            data_user[lst_index[int(i)-1]]["verified"] = True
        with open(path_file_user, "w", encoding="utf-8") as f :
            json.dump(data_user, f,ensure_ascii=False)
        print("Đã xác thực thành công")

def Chinhsua_cauhoi(path_file_question):
    with open(path_file_question,"r",encoding="utf-8") as f :
        data_question = json.load(f)
    idquestion = input("Nhập mã câu hỏi vào đây: ")
    idquestion = Xoa_khoangtrang(idquestion)
    for i in data_question:
        if str(i["ID"]) == idquestion:
            print("Đã tìm thấy câu hỏi")
            ques = Cauhoi(i["ID"],i["question"],i["answer"],i["rightanswer"],i["level"])
            ques.In_cauhoi_admin()
            print("\nBạn muốn thay đổi phần nào\n1: Câu hỏi\n2: Đáp án \n3: Đáp án đúng \n4: Độ khó")
            tmp = input("Nhập vào đây: ")
            tmp = Xoa_khoangtrang(tmp)
            if tmp == "1":
                change = input("Nhập câu hỏi: ")
                ques.question = change
            elif tmp =="2":
                change = input("Nhập đáp án( Lưu ý các đáp án cách nhau bởi dấu \"@;\"): ")
                change = change.split("@;")
                if len(change) != 4:
                    print("Bạn đã nhập thiếu hoặc thừa câu hỏi. Vui lòng nhập lại.")
                    return
                ques.answer = change
            elif tmp =="3":
                change = input("Nhập đáp án đúng vào đây( A, B, C, D): ")
                change = Xoa_khoangtrang(change)
                if change != "A" and change != "B" and change != "C" and change !="D":
                    print("Bạn đã nhập sai. Dừng chương trình.")
                    return
                ques.rightanswer = change
            elif tmp == "4":
                change = input("Nhập độ khó vào đây( BIẾT, HIỂU, VẬN DỤNG THẤP, VẬN DỤNG CAO): ")
                if change != "BIẾT" and change != "HIỂU" and change != "VẬN DỤNG THẤP" and change !="VẬN DỤNG CAO":
                    print("Bạn đã nhập sai. Dừng chương trình.")
                    return
                ques.level = change
            else:
                print("Bạn đã nhập sai cú pháp. Dừng chương trình.")
                return
            i["question"] = ques.question
            i["answer"] = ques.answer
            i["rightanswer"] = ques.rightanswer
            i["level"] = ques.level
            with open(path_file_question, "w", encoding="utf-8") as f:
                json.dump(data_question, f, ensure_ascii=False)
            print("Đã chỉnh sửa thành công")
            return
    else:
        print("Không tìm thấy câu hỏi bạn yêu cầu.")
def Xoa_cauhoi(path_file_question):
    with open(path_file_question,"r",encoding="utf-8") as f :
        data_question = json.load(f)
    idquestion = input("Nhập mã câu hỏi bạn muốn xóa vào đây: ")
    idquestion = Xoa_khoangtrang(idquestion)
    for i in data_question:
        if str(i["ID"]) == idquestion:
            print("Đã tìm thấy câu hỏi")
            ques = Cauhoi(i["ID"],i["question"],i["answer"],i["rightanswer"],i["level"])
            ques.In_cauhoi_admin()
            confirm = input("Bạn có chắc muốn xóa câu hỏi này không? (Nhập 1 để tiếp tục xóa): ")
            confirm = Xoa_khoangtrang(confirm)
            if confirm == "1":
                data_question.remove(i)
            else:
                print("Câu lệnh không hợp lệ. Dừng xóa câu hỏi.")
                return
            with open(path_file_question, "w", encoding="utf-8") as f:
                json.dump(data_question, f, ensure_ascii=False)
            print("Đã xóa câu hỏi thành công.")
            return
    else:
        print("Không tìm thấy câu hỏi. Dừng chương trình")

def Them_cauhoi(path_file_question):
    with open(path_file_question,"r",encoding="utf-8") as f :
        data_question = json.load(f)
    new_ID = input("Nhập mã câu hỏi bạn muốn thêm vào đây: ")
    new_ID = Xoa_khoangtrang(new_ID)
    if not new_ID.isdigit():
        print("ID phải là một số nguyên ")
        return
    for i in data_question:
        if str(i["ID"]) == new_ID:
            print("Đã có ID này rồi. Vui lòng thử lại sau")
            break
    else:
        new_question = input("Nhập câu hỏi mà bạn muốn thêm: ")
        new_answer = input("Nhập đáp án vào đây( Cách nhau bởi \"@;\"): ")
        lst_ans = new_answer.split("@;")
        if len(lst_ans) != 4:
            print("Bạn đã nhập thiếu hoặc thừa đáp án. Vui lòng nhập lại.")
            return
        new_Ranswer = input("Nhập đáp án đúng vào đây( A, B, C, D): ")
        if new_Ranswer != "A" and new_Ranswer != "B" and new_Ranswer != "C" and new_Ranswer !="D":
            print("Bạn đã nhập sai. Dừng chương trình.")
            return
        new_level = input("Nhập độ khó vào đây( BIẾT, HIỂU, VẬN DỤNG THẤP, VẬN DỤNG CAO): ")
        if new_level != "BIẾT" and new_level != "HIỂU" and new_level != "VẬN DỤNG THẤP" and new_level !="VẬN DỤNG CAO":
            print("Bạn đã nhập sai. Dừng chương trình.")
            return
        Cauhoi_moi = Cauhoi(new_ID,new_question, new_answer, new_Ranswer, new_level)
        print("Câu hỏi mới sẽ là: ")
        Cauhoi_moi.In_cauhoi_admin()
        new_data = {"ID": int(new_ID),
                    "question": new_question,
                    "answer": lst_ans,
                    "rightanswer": new_Ranswer,
                    "level": new_level}
        data_question.append(new_data)
        with open(path_file_question, "w", encoding="utf-8") as f:
            json.dump(data_question, f, ensure_ascii=False)
        print("Đã thêm câu hỏi thành công")

def Tao_dethi(path_file_question, file_exam):
    with open(path_file_question,"r",encoding="utf-8") as f :
        data_question = json.load(f)
    n_dokho1 = 0
    n_dokho2 = 0
    n_dokho3 = 0
    n_dokho4 = 0
    index = 0 # sẽ chỉ lưu vị trí của từng độ khó trong dữ liệu ban đầu tránh phải lưu lại câu hỏi
    lst1 = []
    lst2 = []
    lst3 = []
    lst4 = []
    for i in data_question:
        if i["level"] == "BIẾT":
            n_dokho1+=1
            lst1.append(index)
        elif i["level"] == "HIỂU":
            n_dokho2+=1
            lst2.append(index)
        elif i["level"] == "VẬN DỤNG THẤP":
            n_dokho3+=1
            lst3.append(index)
        elif i["level"] == "VẬN DỤNG CAO":
            n_dokho4+=1
            lst4.append(index)
        index += 1
    n = n_dokho1+n_dokho2+n_dokho3+n_dokho4
    print("Trong Ngân hàng câu hỏi có",n, "câu với các độ khó:")
    print(n_dokho1,"câu mức độ Biết")
    print(n_dokho2,"câu mức độ Hiểu")
    print(n_dokho3,"câu mức độ Vận Dụng Thấp")
    print(n_dokho4,"câu mức độ Vận Dụng Cao")

    number_ques1 = input("Nhập số câu hỏi mức độ Biết bạn mong muốn: ")
    number_ques2 = input("Nhập số câu hỏi mức độ Hiểu bạn mong muốn: ")
    number_ques3 = input("Nhập số câu hỏi mức độ Vận Dụng Thấp bạn mong muốn: ")
    number_ques4= input("Nhập số câu hỏi mức độ Vận Dụng Cao bạn mong muốn: ")
    if (number_ques1.isdigit) and (number_ques2.isdigit) and (number_ques3.isdigit) and(number_ques4.isdigit):
        number_ques1 = int(number_ques1)
        if number_ques1 > n_dokho1:
            print("Số lượng câu hỏi mức Biết vượt quá trong ngân hàng câu hỏi")
            return
        number_ques2 = int(number_ques2)
        if number_ques2 > n_dokho2:
            print("Số lượng câu hỏi mức Hiểu vượt quá trong ngân hàng câu hỏi")
            return
        number_ques3 = int(number_ques3)
        if number_ques3 > n_dokho3:
            print("Số lượng câu hỏi mức Vận Dụng Thấp vượt quá trong ngân hàng câu hỏi")
            return
        number_ques4 = int(number_ques4)
        if number_ques4 > n_dokho4:
            print("Số lượng câu hỏi mức Vận Dụng Cao vượt quá trong ngân hàng câu hỏi")
            return
    else:
        print("Bạn phải nhập số nguyên không âm")
    lst_index_ques = []
    for i in range(number_ques1):
        ques_random = random.choice(lst1)
        lst1.remove(ques_random)
        lst_index_ques.append(ques_random)
    for i in range(number_ques2):
        ques_random = random.choice(lst2)
        lst2.remove(ques_random)
        lst_index_ques.append(ques_random)
    for i in range(number_ques3):
        ques_random = random.choice(lst3)
        lst3.remove(ques_random)
        lst_index_ques.append(ques_random)
    for i in range(number_ques4):
        ques_random = random.choice(lst4)
        lst4.remove(ques_random)
        lst_index_ques.append(ques_random)
    lst_Cauhoi = []
    for i in lst_index_ques:
        tmp = data_question[i]
        Cauhoi_moi = Cauhoi(tmp["ID"], tmp["question"],tmp["answer"],tmp["rightanswer"],tmp["level"])
        lst_Cauhoi.append(Cauhoi_moi)
    path_file = input("Bạn muốn lưu đề vào file nào (đuôi txt): ")
    ID = input("Mã của đề mới tạo: ")
    with open(file_exam,"r",encoding="utf-8") as f:
        data_exam = json.load(f)
    for i in data_exam:
        if i["ID"] == ID:
            print("Đã có ID này rồi. Vui lòng thử lại")
            return
    lst_Ranswer = []
    for i in range(len(lst_Cauhoi)):
        lst_Cauhoi[i].In_cauhoi_vaotxt(path_file,i+1)
        lst_Ranswer.append(lst_Cauhoi[i].rightanswer)
    new_exam = {"ID":ID,
                "file":path_file,
                "rightanswer": lst_Ranswer}
    data_exam.append(new_exam)
    with open(file_exam, "w", encoding="utf-8") as f:
        json.dump(data_exam, f, ensure_ascii=False)
    print("Đã tạo đề mới thành công")

def parse_answers(input_str, total_questions):
    # Tách từng mục theo khoảng trắng
    items = input_str.split()
    answers = [None] * total_questions
    # Xử lý từng mục
    for item in items:
        question, answer = item.split('.')
        index = int(question) - 1  # chuyển về chỉ số 0
        if 0 <= index < total_questions:
            answers[index] = answer.upper() # Hàm upper sẽ viết hoa
    return answers

def Lam_de(file_exam,username,file_answers):
    ID = input("Bạn muốn làm đề nào: ")
    with open(file_exam, "r", encoding="utf-8") as f:
        data_exam = json.load(f)
    for i in data_exam:
        if i["ID"] == ID:
            break
    else:
        print("Không tìm thấy đề thi bạn yêu cầu.")
        return
    with open(i["file"],"r",encoding="utf-8") as f:
        data = f.read()
    print("Mã dề thi:",ID)
    print(data)
    total_questions = len(i["rightanswer"])
    print("Nhập đáp án, nếu không có câu trả lời thì bỏ trắng nhập câu khác( VD 1.A 2.B 5.D): ",end = "")
    answers = input("")
    answers = parse_answers(answers,total_questions)
    with open(file_answers,"r",encoding="utf-8") as f :
        data_answer = json.load(f)
    new_data = {
        "ID":ID,
        "username":username,
        "answer": answers,
        "score": None
    }
    data_answer.append(new_data)
    with open(file_answers,"w",encoding="utf-8") as f :
        json.dump(data_answer, f, ensure_ascii=False)
    print("Đã lưu kết quả thi thành công")
def Xem_diem(file_answers, username):
    print("Xin chào",username)
    print("Điểm của bạn: ")
    with open(file_answers,"r",encoding="utf-8") as f :
        data_answer = json.load(f)
    for i in data_answer:
        if i["username"] == username:
            print("Mã đề:",i["ID"],"Điểm:",i["score"])
def Cham_diem(file_answers, file_exam):
    with open(file_answers,"r",encoding="utf-8") as f :
        data_answer = json.load(f)
    with open(file_exam,"r",encoding="utf-8") as f :
        data_exam = json.load(f)
    for i in data_answer:
        if i["score"] == None:
            count = 0
            for j in data_exam:
                if j["ID"] == i["ID"]:
                    lst_Ranswer = j["rightanswer"]
                    total_answer = len(lst_Ranswer)
                    break
            for j in range(total_answer):
                if i["answer"][j] == lst_Ranswer[j]:
                    count += 1
            i["score"] = count/total_answer*10
    with open(file_answers,"w",encoding="utf-8") as f :
        json.dump(data_answer, f, ensure_ascii=False)
    print("Đã chấm điểm thành công")
def Tim_max(lst):
    max = lst[0]
    index = 0
    for i in range(len(lst)):
        if lst[i] > max: 
            max = lst[i]
            index = i
    return max,index
def Tim_min(lst):
    min = lst[0]
    index = 0 
    for i in range(len(lst)):
        if lst[i] <min:
            min = lst[i]
            index = i
    return min, index 
def Tim_avg(lst):
    sum = 0
    for i in lst:
        sum += i
    return sum/(len(lst))
def Tim_phuongsai_hieuchinh(lst,avg):
    sum = 0
    for i in lst:
        sum +=(i-avg)**2
    return sum/(len(lst)-1)
def Lam_tron(lst):
    tmp_lst = []
    for i in lst:
        if i//1+0.5>i:
            tmp_lst.append(int(i//1))
        else:
            tmp_lst.append(int(i//1+1))
    return tmp_lst
def Dem_diem(lst):
    tmp =[0]*11
    for i in lst:
        tmp[i]+=1
    return tmp
def Bao_cao(file_answers, file_exam):
    with open(file_answers,"r",encoding="utf-8") as f :
        data_answer = json.load(f)
    with open(file_exam,"r",encoding="utf-8") as f :
        data_exam = json.load(f)
    ID_exam = input("Nhập ID bài kiểm tra bạn muốn làm báo cáo: ")
    for i in data_exam:
        if i["ID"] == ID_exam:
            print("Đã tìm thấy đề thi")
            exam = i
            break
    else:
        return
    time.sleep(1)
    soluong_traloi = 0
    soluong_cham = 0
    soluong_cauhoi = len(data_answer[0]["answer"])
    lst_answer_dung = [0]*soluong_cauhoi
    lst_score = []
    for i in data_answer:
        if i["ID"] == ID_exam:
            soluong_traloi+=1
            if i["score"] != None:
                soluong_cham +=1
                lst_score.append(i["score"])
                for j in range(soluong_cauhoi):
                    if i["answer"][j] == exam["rightanswer"][j]:
                        lst_answer_dung[j]+=1
    print("Số lượng bài đã làm:",soluong_traloi)
    print("Số lượng bài đã chấm:",soluong_cham)
    if soluong_cham<=1:
        print("Số lượng đề thi đã chấm quá ít xin vui lòng chấm tiếp để đưa ra thông tin phù hợp")
    else:
        max, index_max =Tim_max(lst_answer_dung)
        min, index_min = Tim_min(lst_answer_dung)
        avg = Tim_avg(lst_score)
        s_2 = Tim_phuongsai_hieuchinh(lst_score,avg)
        print("Câu thứ",index_max+1,"có số lượng trả lời đúng nhiều nhất:",max," lượt")
        print("Câu thứ",index_min+1,"có số lượng trả lời đúng ít nhất:",min," lượt")
        print("Điểm trung bình:",avg)
        print("Độ lệch chuẩn hiệu chỉnh:",s_2**(1/2))
        lst_lamtron = Lam_tron(lst_score)
        lst_count = Dem_diem(lst_lamtron)
        max_daudiem, duthua =Tim_max(lst_lamtron)
        for h in range(max_daudiem, 0, -1):
            line = ""
            for value in lst_count:
                if value >= h:
                    line += "█ " # kí hiệu Full Block
                else:
                    line += "  "
            print(line)

        print("―" * (2 * len(lst_count)))
        print(" ".join(str(i) for i in range(len(lst_count))))


    

def Dang_nhap(data_user):
    with open(file_user, "r", encoding="utf-8") as f:
        data_user = json.load(f)
    sign = True
    while sign:
        username = input("Nhập tài khoản: ")
        password = input("Nhập mật khẩu: ")
        for i in data_user:
            if i["username"] == username:
                if i["password"] == password:
                    if i["verified"] == False:
                        print("Tài khoản của bạn chưa được xác thực. Vui lòng chờ xác thực")
                        break
                    sign = False
                    return True, i
                else:
                    print("Mật khẩu bạn đã nhập sai vui lòng nhập lại.")
                    break
        else:
            print("Không có tài khoản "+username)
            turnback = input("Chưa có tài khoản? Nhấn phím 1 để quay lại đăng ký. \nẤn phím bất kỳ để thử lại.\n")
            if turnback == "1":
                return False, None
            
def Giaodien_Bandau():
    print("Chức năng 1: Đăng nhập")
    print("Chức năng 2: Đăng ký tài khoản")
    print("Chức năng 3: Thoát")

def Giaodien_Admin(file_user,file_questions,file_exam,file_answer):
    while True:
        print("\n---- Xin chào Admin ----\n")
        print("Chức năng 1: Phê duyệt tài khoản")
        print("Chức năng 2: Chỉnh sửa câu hỏi")
        print("Chức năng 3: Xóa câu hỏi")
        print("Chức năng 4: Thêm câu hỏi vào ngân hàng câu hỏi")
        print("Chức năng 5: Tạo đề thi ")
        print("Chức năng 6: Chấm điểm")
        print("Chức năng 7: Báo cáo kết quả")
        print("Chức năng 8: Thoát")
        choice = input("Bạn muốn chọn chức năng gì: ")
        if choice == "1":
            Phe_duyet(file_user)
            time.sleep(2)
        elif choice =="2":
            Chinhsua_cauhoi(file_questions)
            time.sleep(2)
        elif choice == "3":
            Xoa_cauhoi(file_questions)
            time.sleep(2)
        elif choice == "4":
            Them_cauhoi(file_questions)
            time.sleep(2)
        elif choice == "5":
            Tao_dethi(file_questions,file_exam)
            time.sleep(2)
        elif choice == "6":
            Cham_diem(file_answer,file_exam)
            time.sleep(2)
        elif choice == "7":
            Bao_cao(file_answer,file_exam)
            time.sleep(2)
        elif choice == "8":
            time.sleep(2)
            break
        else:
            print("Không nhận được yêu cầu phù hợp.")
            time.sleep(2)
def Giaodien_hsinh(file_exam,file_answer,username):
    username = user["username"]
    while True:
        print("\n---- Xin chào "+user["name"]+" ----\n")
        print("Chức năng 1: Làm đề")
        print("Chức năng 2: xem kết quả")
        print("Chức năng 3: Thoát")
        choice = input("Bạn muốn chọn chức năng gì: ")
        if choice == "1":
            Lam_de(file_exam,username,file_answer)
            time.sleep(2)
        elif choice == "2":
            Xem_diem(file_answer,username)
            time.sleep(2)
        elif choice == "3":
            time.sleep(2)
            break
        else:
            print("Không nhận được yêu cầu phù họp")
            time.sleep(2)

file_user = "User.json"
file_questions = "questions.json"
file_exam ="exam.json"
file_answer = "answers.json"
while True:
    print("\n---- Chào mừng tới chương trình quản lý đề thi ----\n")
    Giaodien_Bandau()
    choice = input("Hãy nhập chức năng bạn mong muốn: ")
    if choice == "1":
        retu, user = Dang_nhap(file_user)
        if not retu:
            continue
        else:
            if user["admin"]:
                Giaodien_Admin(file_user,file_questions,file_exam,file_answer)
            else:
                Giaodien_hsinh(file_exam,file_answer,user)
    elif choice == "2":
        Dang_ky(file_user)
    elif choice == "3":
        print("Thoát chương trình.")
        break
    else:
        print("Không hiếu yêu cầu vui lòng nhập lại")

# print(z)
