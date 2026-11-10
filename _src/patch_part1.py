# Clara's Part 1 fixes (5 Oct 2026), simplified for reading level; new sources checked by Claude.
NEW = {
"What does SSAS stand for?": ["SSAS stands for small self-administered scheme. The name comes from tax rules made in 1991. They covered schemes that put at least some of their money outside insurance policies. Where a member was connected with another member, a trustee or the employer, the scheme had to have fewer than 12 members. Those old approval rules ended on 6 April 2006. Today's tax law does not define a SSAS, although the FCA still uses the term."],
"Is a SSAS an occupational pension scheme?": ["Yes. Both the tax law and the pensions law treat it as one. That is because an employer sets it up to provide pensions for people who work for it. The Pensions Regulator oversees the scheme under pensions law. FCA rules can still apply to separate services, such as investment advice or pension transfer advice."],
"Who can set one up?": ["An employer sets up a SSAS. For most people reading this, that is their own company. The scheme administrator then applies online to HMRC to register it. HMRC can ask questions, and it can refuse. For example, it can refuse if a sponsoring employer has been dormant for a whole month in a row during the year before HMRC decides."],
"How many members can a SSAS have?": ["Tax law sets no overall top limit, but 12 is the number that matters. The FCA's description of a SSAS run by its members covers no more than 12 relevant members. And fewer than 12 is the key number for several small-scheme exemptions. If every member is a trustee, and the trustees decide everything together or have an independent trustee, the scheme can be let off some rules. These include having an auditor, the scheme funding rules, and the pension law limits on investing in the employer. HMRC's tax rules still apply."],
"Can my family be members?": ["Yes, if the scheme's rules allow it. But check the tax first. Your company might pay into the SSAS for a family member who does not work for it. If it does so because of a director's or employee's job, the payment is normally taxed on that director or employee. The company normally pays Class 1A National Insurance on it too. If the family member does work for the company, the payment can count as an employer contribution for them. Their pay and pension together should still be fair for the work they do."],
"Can several directors put their pensions into one SSAS?": ["Yes. One SSAS can have several members, such as all the directors. For tax purposes, each member has one or more arrangements in the scheme. In a money purchase arrangement, the member's benefits depend on the pot built up for them. A SSAS with more than one member must register with The Pensions Regulator within three months."],
"Do I need a professional trustee?": ["There is no general rule that every SSAS must have a professional trustee. Before 6 April 2006, the Inland Revenue would only approve a SSAS if one trustee was a pensioneer trustee it had approved. That blanket rule ended in 2006. The Pensions Regulator can still appoint a trustee in special cases. An independent trustee is also one way to qualify for some small-scheme exemptions. The other way is for the member trustees to decide everything together. Some SSAS firms will only run a scheme if they are a trustee too."],
"Are SSAS trustees personally liable if something goes wrong?": ["Yes, they can be. A trustee can have to pay personally for a loss caused by their own breach of trust, and more than one trustee can be liable for the same loss. The trust deed cannot remove liability for failing to take proper care with investments. Some fines and penalties on a trustee cannot be paid from the scheme's money. A trustee who is also the scheme administrator can be liable for tax charges too, such as the scheme sanction charge."],
"Who regulates a SSAS?": ["The Pensions Regulator regulates workplace pension schemes, including SSASs. HMRC registers them and runs the pension tax rules. Running a SSAS is not an FCA-regulated activity in the way running a personal pension is. But FCA rules still apply to separate services, such as managing investments, financial advice and pension transfer advice. Complaints about how a SSAS is run can go to the Pensions Ombudsman. Complaints about financial advice go to the Financial Ombudsman Service."],
"Is a SSAS protected by the FSCS?": ["The scheme itself is not protected if it fails. But cash a SSAS holds in a UK bank can be protected. For a money purchase SSAS, the FSCS can treat each eligible member separately, up to £120,000 per member per banking licence. A member's own savings at the same bank count towards the same limit. If a regulated adviser gave bad pension advice and has since failed, the FSCS may pay up to £85,000."],
"What happens to my SSAS if the provider or administrator goes bust?": ["A SSAS's money and assets are held on trust by its trustees. They do not belong to the firm that does the paperwork. Hartley Pensions went into administration on 29 July 2022. The FCA said the pension assets were held by trustee firms that had not gone bust. But moving to a new administrator can be slow and costly. In July 2026, four years on, Hartley's administrators were still working on a sale or transfer of the SSAS business. They said they needed a court order before they could make clients pay a fee to transfer. Until then, clients could move early if they agreed to pay a fee that would not be refunded."],
"What is the difference between a SSAS and a SIPP?": ["A SIPP is a personal pension, and the firm that runs it needs FCA permission. A SSAS is an occupational pension scheme that a company sets up. Its members are usually its trustees, so they run it together. Both can buy commercial property. A SSAS can also use the special tax rules that allow a loan to its sponsoring employer. A SIPP has no sponsoring employer. If a SIPP lends to a company connected with its member, the loan is an unauthorised payment."],
"Can I move a SIPP into a SSAS?": ["The law allows money to move from one registered pension scheme to another. This is called a recognised transfer, and it can be cash or other assets. Before the money goes, the SIPP firm must run the legal scam checks. For a transfer to an occupational scheme such as a SSAS, you normally need to show a job link with its employer. The evidence is normally a letter from the employer, a schedule of contributions, and three months of payslips or similar salary evidence. A red flag means the transfer cannot go ahead under these rules. An amber flag means you must first have a safeguarding guidance session with MoneyHelper."],
"Can I move a SSAS into a SIPP?": ["Yes. A SIPP is also a registered pension scheme, so this can be a recognised transfer. Assets the SSAS owns, such as business property, can move across as they are (in specie), if the SIPP firm accepts them. Or they can be sold first and the cash moved. An outstanding loanback is different. It does not have to be repaid just because one member transfers. But the loan cannot move into a SIPP if the borrowing company is connected with that member, because that would be an unauthorised payment. If the SSAS carries on, the loan can stay as one of its assets, if its rules and the transfer values allow. If the SSAS is being wound up, the loan must be repaid or dealt with before the last assets leave."],
}
ADD = {
"Is a SSAS an occupational pension scheme?": ["SRC: FCA | Glossary: establishing, operating or winding up a personal pension scheme | https://handbook.fca.org.uk/glossary/G1866"],
"How many members can a SSAS have?": ["SRC: FCA | PERG 10.3.20G: small self-administered schemes | https://www.handbook.fca.org.uk/handbook/PERG/10/?view=chapter"],
"Can my family be members?": ["SRC: HMRC | EIM01570: employer's contributions | https://www.gov.uk/hmrc-internal-manuals/employment-income-manual/eim01570",
                              "SRC: HMRC | NIM13130: Class 1A on benefits for family or household members | https://www.gov.uk/hmrc-internal-manuals/national-insurance-manual/nim13130",
                              "SRC: Law | Social Security Contributions and Benefits Act 1992, s.10 | https://www.legislation.gov.uk/ukpga/1992/4/section/10"],
"Do I need a professional trustee?": ["SRC: Law | Pensions Act 1995, s.7 | https://www.legislation.gov.uk/ukpga/1995/26/section/7"],
"Are SSAS trustees personally liable if something goes wrong?": ["SRC: Law | Pensions Act 2004, s.256 | https://www.legislation.gov.uk/ukpga/2004/35/section/256",
                                                              "SRC: Law | Finance Act 2004, s.239 | https://www.legislation.gov.uk/ukpga/2004/12/section/239"],
"Who regulates a SSAS?": ["SRC: FCA | Glossary: establishing, operating or winding up a personal pension scheme | https://handbook.fca.org.uk/glossary/G1866"],
"Is a SSAS protected by the FSCS?": ["SRC: PRA | PRA Rulebook: Depositor Protection, rule 6.4 | https://www.prarulebook.co.uk/pra-rules/depositor-protection"],
"Can I move a SSAS into a SIPP?": ["SRC: Law | Finance Act 2004, s.161(5) | https://www.legislation.gov.uk/ukpga/2004/12/section/161",
                                   "SRC: HMRC | PTM123300: loans to members and connected parties | https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm123300"],
"What is the difference between a SSAS and a SIPP?": ["SRC: Law | Finance Act 2004, s.161(5) | https://www.legislation.gov.uk/ukpga/2004/12/section/161",
                                                     "SRC: HMRC | PTM123300: loans to members and connected parties | https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm123300"],
}
lines=open('faq.txt',encoding='utf-8').read().splitlines()
out=[];i=0;done=set()
while i<len(lines):
    l=lines[i]
    if l.startswith('## '):
        q=l[3:].strip(); out.append(l); i+=1
        if q in NEW:
            while i<len(lines) and not lines[i].startswith('SRC:'): i+=1
            out.extend(NEW[q]); done.add(q)
        else:
            while i<len(lines) and not lines[i].startswith('SRC:'):
                out.append(lines[i]); i+=1
        # copy SRC lines then add extras
        while i<len(lines) and lines[i].startswith('SRC:'):
            out.append(lines[i]); i+=1
        for extra in ADD.get(q,[]):
            if extra not in out: out.append(extra)
        continue
    out.append(l); i+=1
assert done==set(NEW), set(NEW)-done
open('faq.txt','w',encoding='utf-8').write('\n'.join(out)+'\n')
print('patched',len(done),'answers;',sum(len(v) for v in ADD.values()),'sources added')
