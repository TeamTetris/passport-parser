import re
import sys
import pathlib
import os
import json

from passport import Passport

country_name_re = re.compile('''name_country"><span>(?P<CountryName>.+?)</span>''')
score_re = re.compile('''name_rank"><span>(?P<score>\d+)</span>''')
visa_free_re = re.compile('''<span>Visa-free:</span>\s(?P<VisaFreeValue>\d+)<span>''')
visa_on_arrival_re = re.compile('''<span>Visa on arrival:</span>\s(?P<VisaOnArrival>\d+)<span>''')
visa_required_re = re.compile('''<span>Visa required:</span>\s(?P<VisaRequired>\d+)\"\s>''')

file_path = pathlib.Path(sys.argv[1])

if not file_path.exists():
    print("USAGE: python3 parser.py [FILE PATH]")
    exit(1)

with open(file_path.absolute(), "r") as file:
    file_content = file.read()

country_name_matches = country_name_re.findall(file_content)
score_matches = score_re.findall(file_content)
visa_free_matches = visa_free_re.findall(file_content)
visa_on_arrival_matches = visa_on_arrival_re.findall(file_content)
visa_required_matches = visa_required_re.findall(file_content)

print(f"countries: {len(country_name_matches)}")
print(f"scores: {len(score_matches)}")
print(f"visa free: {len(visa_free_matches)}")
print(f"visa on arrival: {len(visa_on_arrival_matches)}")
print(f"visa required: {len(visa_required_matches)}")

passports = []
for i in range(len(country_name_matches)):
    passport = Passport()
    passport.index = i
    passport.country = country_name_matches[i]
    passport.score = score_matches[i]
    passport.visa_free = visa_free_matches[i]
    passport.visa_on_arrival = visa_on_arrival_matches[i]
    passport.visa_required = visa_required_matches[i]

    passports.append(passport)

output_file_path = pathlib.Path("passports.json")

try:
    os.remove(output_file_path.absolute())
except OSError:
    pass


def obj_dic(obj):
    return obj.__dict__


with open(output_file_path.absolute(), 'w') as file:
    json.dump(obj=passports, fp=file, ensure_ascii=False, indent=4, sort_keys=True, default=obj_dic)

