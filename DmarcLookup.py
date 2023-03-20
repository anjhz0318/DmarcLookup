import argparse
import dns.resolver
import sys

def parser_error(errmsg):
    print(("Usage: python " + sys.argv[0] + " [Options] use -h for help"))
    print(("Error: " + errmsg))
    sys.exit()
def parse_args():
    # parse the arguments
    parser = argparse.ArgumentParser(
        epilog='\tExample: \r\npython ' + sys.argv[0] + " -d example.com")
    parser.error = parser_error
    parser._optionals.title = "OPTIONS"
    parser.add_argument(
        '-d', '--domain', required=True ,help="Enter the domain you want to query.")
    args = parser.parse_args()
    return args

def extract_value(dmarc_record,dmarc_tag):
    #print(dmarc_record)
    tag_length = len(dmarc_tag)
    for element in dmarc_record:
        if element[:tag_length + 1] == dmarc_tag + '=':
            return element[tag_length+1:]
    raise Exception("该域名Dmarc配置不规范")

def query_dmarc_record(domain_name):
    dns_query_result = dns.resolver.resolve(qname="_dmarc."+domain_name, rdtype="TXT", raise_on_no_answer=True)
    dns_response = dns_query_result.response
    answer = dns_response.answer[0].to_text()
    answer = answer.replace('\"', '')
    answer = answer.replace(' ', '')
    print(answer.split(';'))
    record = answer.split(';')
    return record
def main():
    args = parse_args()
    qname = args.domain
    try:
        dmarc_record = query_dmarc_record(qname)
        try:
            p_value = extract_value(dmarc_record,'p')
            if p_value == "none":
                print(f"{qname}的Dmarc配置为none，伪造成功率高！")
            elif p_value == "quarantine":
                print(f"{qname}的Dmarc配置为quarantine，伪造成功率较高！")
            elif p_value == "reject":
                print(f"{qname}的Dmarc配置为reject，伪造成功率低。")
            else:
                print(f"{qname}的Dmarc配置不规范。")
            try:
                sp_value = extract_value(dmarc_record,'sp')
                if sp_value == "none":
                    print(f"{qname}的子域名的Dmarc配置为none，伪造成功率高！")
                elif sp_value == "quarantine":
                    print(f"{qname}的子域名的Dmarc配置为quarantine，伪造成功率较高！")
                elif sp_value == "reject":
                    print(f"{qname}的子域名的Dmarc配置为reject，伪造成功率低。")
                else:
                    print(f"{qname}的子域名的Dmarc配置不规范。")
            except:
                pass
        except:
            print("该域名Dmarc配置不规范")
    except:
        print("Dmarc未配置，伪造成功率高！")

if __name__ == '__main__':
    main()


