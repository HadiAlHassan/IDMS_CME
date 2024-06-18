from pathlib import Path
import pandas as pd

# Get the current directory of the script
current_dir = Path(__file__).resolve().parent

# Define the path to the dataset
dataset_path = current_dir / 'Datasets' / 'terms_definitions.csv'

# Check if the file exists
if not dataset_path.is_file():
    print(f"File not found: {dataset_path}")
else:
    # Load the dataset
    terms_df = pd.read_csv(dataset_path)

    # Classifications based on the provided categories
    court_documents = {
        "Acquittal", "Ad hominem attack", "Admissible", "ADR", "Affirm", "Affirmative defense", "Amicus curiae",
        "Answer", "Appeal", "Appellant", "Appellate court", "Appellee", "Arbitration", "Arraignment", "Assets",
        "Attorney", "Bail", "Bankruptcy", "Bar exam", "Bench trial", "Beyond a reasonable doubt", "Brief", "Burden of proof",
        "Burden of persuasion", "Capital offense", "Case", "Casebook", "Case file", "Case law", "Caseload", "Cause of action/claim",
        "Charge", "Circuit Court", "Circular reasoning", "Citation", "Civil", "Class action", "Clerk of the court", "Code",
        "Common law", "Concurrent sentence", "Concurring opinion", "Consecutive sentence", "Controlling (authority)", "Conviction",
        "Counsel", "Count", "Court", "Court reporter", "Creditor", "Criminal", "DA", "Decision", "De facto", "Default judgment",
        "Defendant", "De jure", "Demurrer", "Deposition", "De novo", "Dicta", "Digests", "Discovery", "Dismissed with prejudice",
        "Dismissed without prejudice", "Disposition", "Dissent", "District court", "Docket", "En banc", "Element/requirement vs. factor/consideration",
        "Evidence", "Exhibit", "Ex parte", "Exclusionary rule", "Exculpatory evidence", "Factor/consideration vs. element/requirement", "Felony",
        "File", "Grand jury", "Guilty/Not guilty", "Habeas corpus", "Headnote", "Hearsay", "Holding", "Hornbook", "Impeachment", "In camera",
        "Inculpatory evidence", "Indictment", "Information", "Injunction", "Intermediate (appellate) court", "IRAC", "Judgment", "Jurisdiction",
        "Jury", "Jury Instructions", "Key number", "Lawsuit", "Lawyer", "Legalese", "LexisNexis", "Liable/Not liable", "Litigation", "Magistrate",
        "MBE", "Misdemeanor", "Mistrial", "Moot", "MPRE", "Negligence", "Nolo contendere", "Non sequitur", "Opinion", "Oral argument", "Outcome determinative",
        "Panel", "Parallel citation", "Parole", "Peremptory challenge", "Persuasive (authority)", "Petit jury", "Plaintiff", "POTUS", "Precedent",
        "Preponderance of the evidence", "Pretrial conference", "Prima facie case", "Primary sources/primary law", "Probation", "Pro bono",
        "Procedural vs. substantive", "Pro se", "Prosecution", "Public defender", "Rationale", "Reasonable inference", "Record", "Regulation",
        "Relevance", "Remand", "Reporter", "Respondent", "Restatement", "Reverse", "Rule statement", "Ruling", "Sanction", "Secondary sources/secondary law",
        "Sentence", "Sequester", "Service", "Service of process", "SCOTUS", "Shepardize", "Slippery slope argument", "Standard of proof", "Stare decisis",
        "Statute", "Statute of limitations", "Strawman argument", "Sua sponte", "Subordination", "Substantive law", "Summary judgment", "Supreme Court",
        "Table of Cases", "Testimony", "Torts", "Transcript", "Treatise", "Trial court", "UCC", "Unannotated code", "Uniform laws", "Unofficial reporter",
        "Uphold", "U.S. Attorney", "Venue", "Verdict", "Voir dire", "Westlaw", "Witness", "Writ", "Writ of certiorari"
    }

    contracts = {
        "Contract", "Arbitration", "Binding (authority)", "Collateral", "Damages", "Equitable", "Equity", "Indemnity",
        "Lease", "Liability", "Mediation", "Settlement"
    }

    legal_forms = {
        "Affidavit", "Complaint", "Deposition", "Interrogatory", "Motion", "Motion in limine", "Motion to dismiss",
        "Petition", "Plea", "Subpoena", "Subpoena duces tecum", "Summons", "Warrant", "Writ"
    }

    # Function to classify words into categories
    def classify_word(word):
        categories = []
        if word in court_documents:
            categories.append('Court Documents')
        if word in contracts:
            categories.append('Contracts')
        if word in legal_forms:
            categories.append('Legal Forms')
        return ' or '.join(categories) if categories else 'Unknown'

    # Apply classification to the dataframe
    terms_df['Category'] = terms_df['Word'].apply(classify_word)

    # Save the updated dataframe to a new CSV file
    output_path = current_dir / 'terms_definition_with_categories.csv'
    terms_df.to_csv(output_path, index=False)

    print(f"Classification completed and saved to '{output_path}'")
