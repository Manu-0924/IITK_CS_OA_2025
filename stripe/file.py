from collections import defaultdict

def trim(string):
    return string.strip()

def split_vec(string):
    return [trim(item) for item in string.split(',')]

def split_set(string):
    return set(trim(item) for item in string.split(','))

def find_fraudulent_merchants(
    non_fraud_codes, fraud_codes, mcc_thresholds, merchant_mcc_map, min_charges, charges
):
    non_fraud = split_set(non_fraud_codes)
    fraud = split_set(fraud_codes)

    # Parse MCC thresholds
    mcc_mp = {}
    for entry in mcc_thresholds:
        temp = split_vec(entry)
        mcc_mp[temp[0]] = float(temp[1])

    # Parse Merchant to MCC mapping
    thresholds_mp = {}
    for entry in merchant_mcc_map:
        temp = split_vec(entry)
        thresholds_mp[temp[0]] = mcc_mp[temp[1]]

    min_transactions = int(min_charges)

    mp = defaultdict(lambda: defaultdict(set))
    transaction_count = defaultdict(int)
    id_act_mp = {}
    fraud_accts = set()

    # Process charges
    for charge in charges:
        temp = split_vec(charge)
        if temp[0] == "CHARGE":
            id_act_mp[temp[1]] = temp[2]
            if temp[4] in fraud:
                mp[temp[2]]["fraud"].add(temp[1])
            else:
                mp[temp[2]]["non_fraud"].add(temp[1])

            transaction_count[temp[2]] += 1

            if transaction_count[temp[2]] < min_transactions:
                continue

            if temp[2] in fraud_accts:
                continue

            ratio = len(mp[temp[2]]["fraud"]) / transaction_count[temp[2]]
            if ratio >= thresholds_mp[temp[2]]:
                fraud_accts.add(temp[2])
        else:  # Handle disputes
            acct = id_act_mp[temp[1]]
            if temp[1] in mp[acct]["fraud"]:
                mp[acct]["fraud"].remove(temp[1])
                mp[acct]["non_fraud"].add(temp[1])

            ratio = len(mp[acct]["fraud"]) / transaction_count[acct]
            if ratio < thresholds_mp[acct]:
                fraud_accts.discard(acct)

    result = ",".join(sorted(fraud_accts))
    return result

if __name__ == "__main__":
    non_fraud_codes = "approved,invalid_pin,expired_card"
    fraud_codes = "do_not_honor,stolen_card,lost_card"

    mcc_thresholds = ["retail,0.8", "venue,0.25"]
    merchant_mcc_map = ["acct_1,retail", "acct_2,retail"]

    min_charges = "2"

    charges = [
        "CHARGE, ch_1, acct_1,100, do_not_honor",
        "CHARGE, ch_2, acct_1,200, lost_card",
        "CHARGE, ch_3, acct_1,300, do_not_honor",
        "DISPUTE, ch_2",
        "CHARGE, ch_4, acct_2,400, lost_card",
        "CHARGE, ch_5, acct_2,500, lost_card",
        "CHARGE, ch_6, acct_1,600, lost_card",
        "CHARGE, ch_7, acct_2,700, lost_card",
        "CHARGE, ch_8, acct_2,800, do_not_honor"
    ]


    result = find_fraudulent_merchants(
        non_fraud_codes, fraud_codes, mcc_thresholds, merchant_mcc_map, min_charges, charges
    )
    print(result)  # Output: acct_1,acct_3
