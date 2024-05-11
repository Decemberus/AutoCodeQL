import json
import os


def extract_vulnerabilities(sarif_file):
    with open(sarif_file, 'r') as f:
        data = json.load(f)

    all_messages = []
    for run in data['runs']:
        for result in run['results']:
            if 'codeFlows' in result:
                for codeFlow in result['codeFlows']:
                    messages = []
                    for threadFlow in codeFlow['threadFlows']:
                        for location in threadFlow['locations']:
                            message = location['location']['message']['text']
                            messages.append(message)
                    if messages:
                        messages[0] = "source: " + messages[0]
                        messages[-1] = "sink: " + messages[-1]
                    for i in range(1,len(messages) - 1):
                        messages[i] = f"dataflow{i}: " + messages[i]

                    all_messages.append(messages)

    outputprinting(all_messages)

def outputprinting(all_messages):
    if not os.path.exists('../result/'):
        os.makedirs('../result/')

    try:
        #with open('../result/finalresult.txt', 'w') as f:
        with open('./finalresult.txt', 'w') as f:
            for i, messages in enumerate(all_messages):
                f.write(f"CodeFlow {i+1}:\n")
                print(f"CodeFlow {i+1}:")
                for m in messages:
                    f.write(m)
                    f.write('\n')
                    print(m)
                print()
                f.write('\n')

        print("结果已保存至：", './finalresult.txt')
    except Exception as e:
        print(f"Error: {e}")

