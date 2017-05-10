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

def fill_orders(order_list, resource_avail):
    output = {"remaining_cookies": resource_avail, "unfulfilled_orders":[]}

    for entry in order_list:
        if(entry["amt"] > output["remaining_cookies"]):
            (output["unfulfilled_orders"]).append(entry["id"])

        elif(entry["amt"] <= output["remaining_cookies"]):
            output["remaining_cookies"] = output["remaining_cookies"] - entry["amt"]
            entry["fulfilled"] = True

    (output["unfulfilled_orders"]).sort()

    return output


def main(argv):
    input_args = get_inputs()
    page_info = get_resource_info(input_args.url[0])
    json_pages = get_paginated(input_args.url[0], page_info['num_pages'])
    trimmed_json = trim_orders(json_pages, input_args.otyp)
    prioritized = sort_orders(trimmed_json, input_args.srt)
    results = fill_orders(prioritized, page_info['resource_avail'])

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main(sys.argv[1:])