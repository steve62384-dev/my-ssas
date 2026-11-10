# Clara's Part 3 fixes (5 Oct 2026), simplified for reading level.
NEW = {
"When can I take money out?": ["Normally from age 55. From 6 April 2028 this goes up to 57. You may be able to start sooner if medical evidence shows you cannot carry on your job because of illness or disability, and you stop doing that job. You may also have a protected pension age. If its rules allow, a SSAS can pay out in several ways. These include a tax-free lump sum, money taken out bit by bit (drawdown), a scheme pension, or buying an annuity."],
"How much can I take tax free?": ["Usually, up to 25% of the pension benefits you take can be tax free. For most people there is also an overall lump sum allowance of £268,275 across all their pensions. That limit has applied since 6 April 2024. Some people with older protections can take more. The rest is taxed as income when it is paid out."],
"What happens to my SSAS if I die before 75?": ["If you die before 75, many death benefits can be paid without income tax. A lump sum is normally tax free up to your available lump sum and death benefit allowance, usually £1,073,100. It must be paid within two years of when the scheme first knew, or could reasonably have known, of your death. Drawdown for a dependant or nominee is also usually tax free, if its conditions are met. A dependants' scheme pension is always taxed as income. From 6 April 2027, inheritance tax may also apply."],
"What happens if I die at 75 or over?": ["The people who get your SSAS money pay income tax on it, at their own tax rate. If a taxable lump sum is paid to a company, or to trustees (other than bare trustees), the scheme administrator normally pays a 45% charge instead. From 6 April 2027, inheritance tax may apply as well. But income tax is not charged on the part used to pay the inheritance tax."],
"What is a dependants' scheme pension, and why does it matter?": ["It is a regular income the scheme pays to a dependant after a member dies. A dependant includes a husband, wife or civil partner, or a child under 23. In some cases it includes another person who relied on the member financially. A child aged 23 or over normally counts only if they depended on the member because of a physical or mental impairment. The dependant pays income tax on the pension.", "It matters because of inheritance tax. From 6 April 2027, pension money is left out of inheritance tax only if it may only be used to pay a dependants' scheme pension. If the person can choose another kind of death benefit instead, it is not left out."],
"Does HMRC still register new SSASs, and why does it refuse some?": ["Yes. The law says HMRC must register a new pension scheme unless certain problems apply. One is wrong or false information. Another is a scheme not set up mainly to provide authorised pensions or lump sums. Others are a scheme administrator who is not fit and proper, or a sponsoring company that has been dormant for a month in a row in the past year. HMRC does refuse many. Its April 2026 newsletter says it received 2,421 applications to register new pension schemes in 2025/26. It registered 54%, refused 33%, and had not yet decided the rest. Those figures cover all kinds of scheme, not just SSASs."],
"What does the trustee have to do each year?": ["Keep clear records. Keep them for the tax year they relate to and six more years. File with HMRC when needed. That means an event report by 31 January if certain events happened, and a pension scheme return if HMRC sends a notice to file. It also means an Accounting for Tax return if certain tax charges arise. A money purchase SSAS with 2 to 11 members normally completes a scheme return for The Pensions Regulator every three years. A final salary (defined benefit) scheme completes one every year. A small SSAS needs no auditor, if every member is a trustee and the trustees decide everything together or have an independent trustee."],
"What happens if my company closes?": ["A SSAS does not end just because the company closes, unless its rules say so. The trustees may be able to run it as a closed scheme, or they may wind it up. HMRC can take a SSAS off its register if a sponsoring employer is a dormant company. If HMRC does de-register it, the scheme administrator faces a charge of 40% of the cash and the market value of the assets held just before. If the SSAS is wound up, HMRC must be told within three months of the wind up finishing."],
"What are the disadvantages of a SSAS?": ["A SSAS costs money to set up and run each year. The fees are flat, so they weigh more on a small pension. The trustees, often the members themselves, must follow pension and tax law. They can be personally liable for losses they cause. Breaking the tax rules is costly. An unauthorised payment normally causes a 40% tax charge on the member or employer. A further 15% surcharge can apply if enough unauthorised payments are made. The scheme administrator can also face a scheme sanction charge: normally 15% where the 40% charge has been paid, but up to 40% otherwise. A loan to your own company can go wrong. And the FSCS cannot protect the scheme itself if it fails. See <a href=\"/ssas-disadvantages/\">the full list of disadvantages</a>."],
}
ADD = {
"When can I take money out?": ["SRC: Law | Finance Act 2004, Sch 28, para 1 | https://www.legislation.gov.uk/ukpga/2004/12/schedule/28"],
"How much can I take tax free?": ["SRC: Law | Income Tax (Earnings and Pensions) Act 2003, ss.637P and 637Q | https://www.legislation.gov.uk/ukpga/2003/1/section/637P"],
"What happens to my SSAS if I die before 75?": ["SRC: HMRC | PTM073100: lump sum death benefits | https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm073100",
    "SRC: HMRC | Technical note: Inheritance Tax on pensions | https://www.gov.uk/government/publications/inheritance-tax-on-pensions-technical-note/technical-note-inheritance-tax-on-pensions"],
"Does HMRC still register new SSASs, and why does it refuse some?": [],
"What happens if my company closes?": [],
"What are the disadvantages of a SSAS?": ["SRC: Law | Finance Act 2004, ss.208, 209, 239 and 240 | https://www.legislation.gov.uk/ukpga/2004/12/section/240",
    "SRC: HMRC | PTM131000: unauthorised payments | https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm131000",
    "SRC: HMRC | PTM135100: scheme sanction charge | https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm135100"],
}
lines=open('faq.txt',encoding='utf-8').read().splitlines()
out=[];i=0;done=set()
while i<len(lines):
    l=lines[i]; out.append(l); i+=1
    if l.startswith('## '):
        q=l[3:].strip(); block=[]
        while i<len(lines) and not lines[i].startswith('## ') and not lines[i].startswith('# '):
            if lines[i].strip(): block.append(lines[i])
            i+=1
        srcs=[b for b in block if b.startswith('SRC:')]
        paras=[b for b in block if not b.startswith('SRC:')]
        if q in NEW: paras=NEW[q]; done.add(q)
        for extra in ADD.get(q,[]):
            if extra not in srcs: srcs.append(extra)
        out.extend(paras+srcs); out.append('')
assert done==set(NEW), set(NEW)-done
open('faq.txt','w',encoding='utf-8').write('\n'.join(out).rstrip()+'\n')
print('patched',len(done))
