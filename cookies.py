import json, requests, operator, sys, getopt, argparse, pdb


def get_inputs():
    # Should add functionality to screen user input(eg: what are acceptable otypes)
    # Perhaps also functionality to add an otype to some file that defines acceptable otypes
    url = ''
    sort_by = []
    order_type = ''
    output_file = ''

    parser = argparse.ArgumentParser(description="query paginated JSON orders, sort specified order type by specified fields")

    parser.add_argument('--url', type=str, nargs="+", help='url of JSON to get')

    parser.add_argument('--srt', nargs="+", help='list of sorting criteria')

    parser.add_argument('--otyp', type=str, nargs='+', help='order type to be filled (eg: Cookie, pudding, etc)')

    parser.add_argument('--fill', action='store_true', default=False, help="Include --fill flag to specify order fill action once sorted")

    args = parser.parse_args()

    return(args)


def get_resource_info(url):
    data = requests.get(url).json()

    # Would be nice to make these more general
    num_pages = data['pagination']['total']
    resource_avail = data["available_cookies"]

    page_info = {"num_pages": num_pages, "resource_avail": resource_avail}

    return page_info


def get_paginated(url, num_pages):
    results = []

    for page in range(1, num_pages+1):
        response = requests.get(url, params={'page': page}).json()


        results.append(response)

    return results

def trim_orders(all_orders, otype):
    trimmed_orders = []

    for page in all_orders:
        for key, val in page.items():
            if(key == "orders"):
                for i in val:
                    if(i["fulfilled"] == False):
                        for prod in i["products"]:
                            if(prod["title"] == otype[0]):
                                order = {}
                                order["id"] = i["id"]
                                order["amt"] = prod["amount"]
                                order["fulfilled"] = False
                                trimmed_orders.append(order)

    return trimmed_orders

# Sort vars need param to define ascend/descend for each var
# 
def sort_orders(ords_to_fill, sort_vars):
    ords_to_fill.sort(key=operator.itemgetter(sort_vars[1]))
    ords_to_fill.sort(key=operator.itemgetter(sort_vars[0]), reverse=True)

    return ords_to_fill

def out_putter(order_list, resource_avail, fill_now):
    output = {"remaining_cookies": resource_avail, "unfulfilled_orders":[]}

    if(fill_now):
        for entry in order_list:
            if(entry["amt"] > output["remaining_cookies"]):
                (output["unfulfilled_orders"]).append(entry["id"])

            elif(entry["amt"] <= output["remaining_cookies"]):
                output["remaining_cookies"] = output["remaining_cookies"] - entry["amt"]
                entry["fulfilled"] = True

        (output["unfulfilled_orders"]).sort()

    else:
        for entry in order_list:
            (output["unfulfilled_orders"]).append(entry["id"])


    #(output["unfulfilled_orders"]).sort()

    return output


def main(argv):
    input_args = get_inputs()
    url = input_args.url[0]
    order_type = input_args.otyp
    sort_param = input_args.srt
    order_fill_bool = input_args.fill

    page_info = get_resource_info(url)

    num_pages = page_info['num_pages']
    resource_avail =  page_info['resource_avail']

    json_pages = get_paginated(url, num_pages)
    trimmed_json = trim_orders(json_pages, order_type)
    prioritized = sort_orders(trimmed_json, sort_param)
    results = out_putter(prioritized, resource_avail, order_fill_bool)

    print(json.dumps(prioritized, indent=2))
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main(sys.argv[1:])