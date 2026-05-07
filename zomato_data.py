





import json
from rich import print

with open(r"C:\Users\kishan.prajapati\Desktop\actowiz_work\6_day task_regex\main_zomato.json",'r',encoding='utf-8') as f:
    data=json.load(f)
    

basic_info=data['page_data']['sections']['SECTION_BASIC_INFO']
cont_info=data['page_data']['sections']['SECTION_RES_CONTACT']
fssai_lc_num=data['page_data']['order']['menuList']['fssaiInfo']
cuisune_info=data['page_data']['sections']['SECTION_RES_HEADER_DETAILS']['CUISINES']
menu_info=data['page_data']['order']['menuList']['menus']
item_path=data['page_data']['order']['menuList']['menus']
days = ["monday", "tuesday", "wednesday", "thursday","friday", "saturday"]

restaurant_data={
    "restaurant_id":"",
    "restaurant_name":"",
    "restaurant_url":"",
    "restaurant_contact":[""],
    "fssai_licence_number":"",
    "address_info":{},
    "cuisines":[],
    "timings":{},
    "menu_categories":[]
    
    }

restaurant_data['restaurant_id']=basic_info.get('res_id')
restaurant_data['restaurant_name']=basic_info.get('name')
restaurant_data['restaurant_url']="https://www.zomato.com"  +  basic_info.get('resUrl','')
restaurant_data['restaurant_contact']=[cont_info['phoneDetails'].get('phoneStr')]
restaurant_data['fssai_licence_number']=fssai_lc_num.get('text')
restaurant_data['address_info']={
    "full_address": cont_info.get('address',''),
    "region": cont_info.get('locality_verbose', '') ,
    "city": cont_info.get('city_name',''),
    "pincode": cont_info.get('zipcode',''),
    "state": "Gujarat" 
}

for cuis in cuisune_info:
    restaurant_data['cuisines'].append({
        "name":cuis.get('name',''),
        "url":cuis.get('url','')
    })
    

time_data=basic_info['timing']['customised_timings']['opening_hours']

for day in days:
    for t in time_data:
        days=  t['days']
        timing= t['timing']
        restaurant_data['timings'][day] = {
            "open_time" : timing.split(" ")[0].strip(),
            "close_time" : timing.split(" ")[-1].strip()
        }

    
for menu_data in menu_info:
    menu=menu_data['menu']
    category=menu['name']
    
    
    for cat in menu['categories']:
        items=cat['category']['items']
        category_name = cat['category']['name']
        rest_data = []
        
        for it in items:   
            item_name = it['item']['name']
            item_id = it['item']['id']
            item_url = it['item']['item_image_url']
            item_description = it['item']['desc']
            item_price = float(0)
            item_isveg = bool()
            item_slug=it['item']['dietary_slugs']
            rest_data.append({
                "item_id": item_id, 
                "item_name": item_name,
                "item_slugs": item_slug,
                "item_url": item_url,
                "item_description": item_description,
                "item_price": item_price,
                "is_veg": item_isveg
                
            })
        restaurant_data['menu_categories'].append({
            'category_name': category_name,
            'items': rest_data
        })
        
        
                  
#print(json.dumps(restaurant_data, indent=4, ensure_ascii=False))
with open(r'new_zomato.json','w',encoding='utf-8') as f:
    json.dump(restaurant_data,f,indent=4)