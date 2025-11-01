import requests
import time
import itertools
import random
import os
import json    
name2case={"一代手套": 5, "二代手套": 1, "三代手套": 117, "多普勒爪": 3, "多普勒蝶": 15, "渐变锯齿": 19, "多普勒锯齿": 36, "伽马爪": 46, "渐变骷髅": 86, "一代蝴蝶": 87, "渐变爪": 94, "伽马蝶": 138, "尼泊尔": 300, "多普勒骷髅": 484}
url="https://api.csqaq.com/api/v1"
with open("config","r",encoding="utf-8") as f:
    config=json.load(f)
api_key=config['api_key']
def get_case():
    URL=f"{url}/info/container_data_info"
    headers={
        "ApiToken":api_key
    }
    payload={}
    response = requests.request("POST", URL, headers=headers, data=payload).json()
    print(response['msg'])
    time.sleep(0.9)
    return response
def get_list(id):
    URL=f"{url}/info/good/container_detail"
    params={"id":id}
    headers={
        "ApiToken":api_key
    }
    payload={}
    response=requests.request("GET", URL, headers=headers, data=payload, params=params).json()
    print(response['msg'])
    time.sleep(0.9)
    return response
def get_hashname(name):
    URL =f"{url}/info/get_good_id"
    payload = json.dumps({
        "page_index": 1,
        "page_size": 1,
        "search": name
    })
    headers = {
        'ApiToken': api_key,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", URL, headers=headers, data=payload).json()
    if(response['msg']!="Success"):
        print(response)
    else:
        print(f"✅ 成功获取物品: {name}")
    time.sleep(0.9)
    return response
def get_price(marketHashNameList):
    URL =f"{url}/goods/getPriceByMarketHashName"
    payload = json.dumps({
        "marketHashNameList": marketHashNameList
    })
    headers = {
        'ApiToken': api_key,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", URL, headers=headers, data=payload).json()
    if(response['msg']!="Success"):
        print(response)
    else:
        print(f"✅ 成功获取价格信息")
    time.sleep(0.9)
    return response
to_search=[5,1,117,87,94,36,46,3,15,138,484,19,86]
material=[""]*500
cases=[""]*500
cases[5]="一代手套"
cases[1]="二代手套"
cases[117]="三代手套"
cases[3]="多普勒爪"
cases[15]="多普勒蝶"
cases[19]="渐变锯齿"
cases[36]="多普勒锯齿"
cases[46]="伽马爪"
cases[86]="渐变骷髅"
cases[87]="一代蝴蝶"
cases[94]="渐变爪"
cases[138]="伽马蝶"
cases[300]="尼泊尔"
cases[484]="多普勒骷髅"
material[5]="Five-SeveN | Hyper Beast"
material[1]="AK-47 | Head Shot"
material[117]="USP-S | The Traitor"
material[3]="M4A1-S | Chantico's Fire"
material[15]="AK-47 | The Empress"
material[19]="Desert Eagle | Code Red"
material[36]="Glock-18 | Bullet Queen"
material[46]="FAMAS | Roll Cage"
material[86]="MAC-10 | Stalker"
material[87]="P90 | Asiimov"
material[94]="R8 Revolver | Fade"
material[138]="AK-47 | Nightwish"
material[300]="AWP | Chrome Cannon"
material[484]="FAMAS | Bad Trip"
namehash={
    "折刀（★）":"★ Navaja Knife",
    "熊刀（★）":"★ Ursus Knife",
    "短剑（★）":"★ Stiletto Knife",
    "锯齿爪刀（★）":"★ Talon Knife",
    "弯刀（★）":"★ Falchion Knife",
    "骷髅匕首（★）":"★ Skeleton Knife",
    "蝴蝶刀（★）":"★ Butterfly Knife",
    "流浪者匕首（★）":"★ Nomad Knife",
    "求生匕首（★）":"★ Survival Knife",
    "系绳匕首（★）":"★ Paracord Knife",
    "爪子刀（★）":"★ Karambit",
    "M9 刺刀（★）":"★ M9 Bayonet",
    "刺刀（★）":"★ Bayonet",
    "穿肠刀（★）" :"★ Gut Knife",
    "折叠刀（★）":"★ Flip Knife",
    "廓尔喀刀（★）":"★ Kukri Knife",
    "鲍伊猎刀（★）":"★ Bowie Knife",
}
def get_product():
    for i in to_search:
        data=get_list(i)['data']
        data=[item for item in data if item['qln']=="★"]
        seen = set()
        data = [item for item in data if not (item['short_name'] in seen or seen.add(item['short_name']))]
        
        with open(f"case/case_{i}.json","w",encoding="utf-8") as f:
            json.dump(data,f,ensure_ascii=False,indent=4)
def get_namehash():
    for i in to_search:
        with open(f"case/case_{i}.json","r",encoding="utf-8") as f:
            data=json.load(f)
            
            # 先收集所有market_hash_name，再一次性写入
            all_market_names = []
            locked_float_names1 = ['伽马多普勒','多普勒','渐变','虎牙','屠夫']
            for item in data:
                name = item['short_name']
                if(item['rln']=='非凡'):
                    name += ' (久经沙场)'
                else:
                    if('外表生锈' in name):
                        name += ' (战痕累累)'
                    elif(any(x in name for x in locked_float_names1)):
                        name += ' (崭新出厂)'
                    elif('|'in name):
                        name += ' (久经沙场)'
                    else:
                        all_market_names.append(namehash[name])
                        continue
                response = get_hashname(name)
                data_dict = response['data']['data']

                first_item = list(data_dict.values())[0]
                market_hash_name = first_item['market_hash_name']
                all_market_names.append(market_hash_name)
                
            
            # 一次性写入所有market_hash_name
            with open(f"name/name_{i}久经沙场.json","w",encoding="utf-8") as g:
                json.dump(all_market_names, g, ensure_ascii=False, indent=4)
            all_market_names = []
            for item in data:
                name = item['short_name']
                if(item['rln']=='非凡'):
                    name += ' (略有磨损)'
                else:
                    if('外表生锈' in name):
                        name += ' (战痕累累)'
                    elif(any(x in name for x in locked_float_names1)):
                        name += ' (崭新出厂)'
                    elif('|'in name):
                        name += ' (略有磨损)'
                    else:
                        all_market_names.append(namehash[name])
                        continue
                response = get_hashname(name)
                data_dict = response['data']['data']
                
                # 添加错误处理
                if data_dict and len(data_dict) > 0:
                    first_item = list(data_dict.values())[0]
                    market_hash_name = first_item['market_hash_name']
                    all_market_names.append(market_hash_name)
                else:
                    print(f"❌ 未找到物品: {name}")
                
            
            # 一次性写入所有market_hash_name
            with open(f"name/name_{i}略有磨损.json","w",encoding="utf-8") as g:
                json.dump(all_market_names, g, ensure_ascii=False, indent=4)

output_data = {
    "更新时间": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
    "期望数据": []
}
def _breakeven_by_enumeration(case_name, num_crafts, single_cost):
    """使用枚举方法计算保本率"""
    n=0
    total_cost = single_cost * num_crafts
    all_prices = []
    with open(f"price/price_{case_name}.json","r",encoding="utf-8") as f:
        data = json.load(f)
        all_prices = [item['yyypSellPrice'] for item in data.values()]
        n = len(all_prices)
    total_combinations = n ** num_crafts
    profitable_count = 0
    
    # 枚举所有可能的锻刀结果组合
    for combination in itertools.product(all_prices, repeat=num_crafts):
        total_revenue = sum(combination)
        if total_revenue > total_cost:
            profitable_count += 1
    expectation = sum(all_prices) / n / single_cost
    breakeven_rate = profitable_count / total_combinations if total_combinations > 0 else 0
    return breakeven_rate, expectation
def update_prices():
    output_data["更新时间"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    for i in to_search:
        with open(f"name/name_{i}久经沙场.json","r",encoding="utf-8") as f:
            marketHashNameList=json.load(f)
            if(len(marketHashNameList)>50):
                marketHashNameList1=marketHashNameList[:50]
                marketHashNameList2=marketHashNameList[50:]
                data1=get_price(marketHashNameList1)['data']['success']
                data2=get_price(marketHashNameList2)['data']['success']
                data={**data1,**data2}
            else:
                data=get_price(marketHashNameList)['data']['success']
            with open(f"price/price_{i}久经沙场.json","w",encoding="utf-8") as g:
                json.dump(data,g,ensure_ascii=False,indent=4)
            
        with open(f"name/name_{i}略有磨损.json","r",encoding="utf-8") as f:
            marketHashNameList=json.load(f)
            if(len(marketHashNameList)>50):
                marketHashNameList1=marketHashNameList[:50]
                marketHashNameList2=marketHashNameList[50:]
                data1=get_price(marketHashNameList1)['data']['success']
                data2=get_price(marketHashNameList2)['data']['success']
                data={**data1,**data2}
            else:
                data=get_price(marketHashNameList)['data']['success']
            with open(f"price/price_{i}略有磨损.json","w",encoding="utf-8") as g:
                json.dump(data,g,ensure_ascii=False,indent=4)
        

# 收集数据并保存到output.json
def compute_expectations():
    for i in to_search:
        case_data = {}
        
        # 久经沙场
        with open(f"price/price_{i}久经沙场.json","r",encoding="utf-8") as f:
            data = json.load(f)
            material_name = []
            material_name.append(material[i] + " (Field-Tested)")
            material_price = get_price(material_name)['data']['success'][material[i] + " (Field-Tested)"]['yyypSellPrice']
            
            # 单次锻刀保本率
            single_breakeven_rate = sum(item['yyypSellPrice'] / material_price / 4.9 > 1 for item in data.values()) / len(data.values())
            
            three_times_breakeven_rate = _breakeven_by_enumeration(f"{i}久经沙场", 3, material_price * 4.9)[0]
            
            prices = [item['yyypSellPrice'] for item in data.values()]
            avg_price = sum(prices) / len(prices) if prices else 0
            
            case_data["久经沙场"] = {
                "期望收益": avg_price,
                "材料参考底价": material_price,
                "单次锻刀期望": avg_price / material_price / 5.0,
                "单次锻刀保本率": single_breakeven_rate,
                "三次连续锻刀保本率": three_times_breakeven_rate,
            }
        
        # 略有磨损
        with open(f"price/price_{i}略有磨损.json","r",encoding="utf-8") as f:
            data = json.load(f)
            material_name = []
            material_name.append(material[i] + " (Minimal Wear)")
            material_price = get_price(material_name)['data']['success'][material[i] + " (Minimal Wear)"]['yyypSellPrice']

            single_breakeven_rate = sum(item['yyypSellPrice'] / material_price / 5.5 > 1 for item in data.values()) / len(data.values())
            
            three_times_breakeven_rate = _breakeven_by_enumeration(f"{i}略有磨损", 3, material_price * 5.5)[0]
            
            prices = [item['yyypSellPrice'] for item in data.values()]
            avg_price = sum(prices) / len(prices) if prices else 0
            
            case_data["略有磨损"] = {
                "期望收益": avg_price,
                "材料参考底价": material_price,
                "单次锻刀期望": avg_price / material_price / 5.0,
                "单次锻刀保本率": single_breakeven_rate,
                "三次连续锻刀保本率": three_times_breakeven_rate,
            }
        
        output_data["期望数据"].append({
            "箱子名称": cases[i],
            "数据": case_data
        })


    # 将结果保存到output.json
    with open("期望.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)
    
    print("数据已保存到 期望.json")

def simulate():
    """模拟锻刀过程"""
    print()
    print("锻刀模拟器")
    print()
    
    # 获取用户输入
    try:
        single_cost = float(input("请输入单次锻刀成本: ").strip())
        case_name = input("请输入产物名称: ").strip()
        floatlv = input("请输入磨损类型 (久经沙场/略有磨损): ").strip()
        case_name= f"{name2case[case_name]}"
    except ValueError:
        print("错误: 请输入有效的数字！")
        return
    
    # 构建文件路径
    filename = f"price/price_{case_name}{floatlv}.json"
    
    # 检查文件是否存在
    if not os.path.exists(filename):
        print(f"错误: 找不到文件 {filename}")
        return
    
    # 加载价格数据
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"错误: 读取文件失败 - {e}")
        return
    
    # 获取所有可能的产物和价格
    products = list(data.values())
    if not products:
        print("错误: 价格数据为空")
        return
    
    # 初始化统计信息
    total_cost = 0
    total_revenue = 0
    simulation_count = 0
    profitable_count = 0
    
    print(f"\n开始模拟锻刀 - {case_name} ({floatlv})")
    print(f"单次成本: {single_cost}")
    print("输入 1 进行锻刀，输入 0 退出模拟")
    print("-" * 40)
    
    while True:
        user_input = input("是否进行锻刀？ (1=继续, 0=退出): ").strip()
        
        if user_input == "0":
            break
        elif user_input == "1":
            # 随机选择一种产物
            selected_product = random.choice(products)
            product_price = selected_product.get('yyypSellPrice', 0)
            product_name = selected_product.get('name', '未知产物')
            # 更新统计
            total_cost += single_cost
            total_revenue += product_price
            simulation_count += 1
            
            if product_price > single_cost:
                profitable_count += 1
            
            # 显示本次结果
            print(f"\n第{simulation_count}次锻刀结果:")
            print(f"成本: {single_cost:.2f}")
            print(f"产物名称: {product_name}")
            print(f"产物价值: {product_price:.2f}")
            print(f"本次收益: {product_price - single_cost:.2f}")
            
            # 显示累计统计
            print(f"\n累计统计:")
            print(f"锻刀次数: {simulation_count}")
            print(f"总成本: {total_cost:.2f}")
            print(f"总收益: {total_revenue:.2f}")
            print(f"总利润: {total_revenue - total_cost:.2f}")
            print(f"保本率: {profitable_count/simulation_count*100:.1f}%")
            print("-" * 30)
            
        else:
            print("无效输入，请输入 1 或 0")
        
def main_menu():
    """主菜单"""
    print("锻刀收益计算器启动成功！")
    

    while True:
        print()
        print("锻刀收益计算器")
        print()
        print("1. 更新价格数据")
        print("2. 批量计算期望")
        print("3. 计算保本率")
        print("4. 锻刀模拟器")
        print("5. 输出产物名称列表")
        print("6. 退出程序")
        print()
        
        choice = input("请选择操作 (1-6): ").strip()
        
        if choice == "1":
            update_prices()
        elif choice == "2":
            compute_expectations()
        elif choice == "3":
            print("\n计算保本率（枚举法）")
            case_name = input("请输入产物名称: ").strip()
            floatlv=input("请输入磨损类型 (久经沙场/略有磨损): ").strip()
            case_name= f"{name2case[case_name]}{floatlv}"
            try:
                num_crafts = int(input("锻刀次数: ").strip())
                single_cost = float(input("单次锻刀成本: ").strip())
                breakeven_rate, expectation = _breakeven_by_enumeration(case_name, num_crafts, single_cost)
                print(f"{num_crafts}次锻刀保本率：{breakeven_rate:.2%}，期望：{expectation:.3f}")
            except ValueError:
                print("错误: 请输入有效的数字！")
        elif choice == "4":
            simulate()
        elif choice == "5":
            print("\n产物名称列表:")
            for key, value in name2case.items():
                print(key)
        elif choice == "6":
            print("感谢使用，再见！")
            break
        else:
            print("无效选择，请输入 1-5 之间的数字")

if __name__ == "__main__":
    main_menu()