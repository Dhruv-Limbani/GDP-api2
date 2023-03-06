base_url_get_lkysyms = "https://general-disease-pred-api.onrender.com/get_lksyms?"
get_lkysyms = "/get_lkysyms"
#sym_list=cough&sym_list=chills&sym_list=headache
syms = []
ok = False
while(ok!=True):
    syms.append(input("Enter symptom: "))
    ok = True if input("any other symptom: ") == 'no' else False
cust_url = base_url_get_lkysyms
for s in syms:
    cust_url = cust_url + f"sym_list={s}&"
cust_url = cust_url[:-1]

print(cust_url)