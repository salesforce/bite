import csv, argparse, os, re

parser = argparse.ArgumentParser()
parser.add_argument(
        "--data_file", default=None, type=str, required=True, help="The input data file (a text file)."
    )
parser.add_argument("--output_dir", default=None, type=str, required=True)
args = parser.parse_args()

with open(args.data_file,'r') as in_file:
    with open(os.path.join(args.output_dir,args.data_file.split('/')[-1]+'.proc'),'w') as out_file:
        reader = csv.reader(in_file, delimiter='\t')
        next(reader)
        sentences = []
        for row in reader:
            if row[1] != 'misc':
                speaker = row[1].split('_')[1]
                if speaker == 'int':
                    continue
            if row[3][:6] == '(pause':
                continue
            #print(row[3])
            s = re.sub(r'<(.*?)>', '', row[3])
            s = re.sub(r'\((.*?)\)', '', s)
            s = re.sub(r'/\?(.*?)/', '', s)
            s = s.replace('[','').replace(']','').replace('/unintelligible/','').replace('/','').replace('  ',' ').strip()
            if not s:
                continue
            if sentences and s[0].islower():
                sentences[-1] += ' ' + s
            elif sentences and sentences[-1][-1] in ',-':
                sentences[-1] += ' ' + s
            else:
                sentences.append(s)
        for s in sentences:
            if len(s.split()) > 3:
                out_file.write(s + '\n')
