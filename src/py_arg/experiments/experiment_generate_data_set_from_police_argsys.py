import random

from py_arg.experiments.utils import path_to_resources
from py_arg.incomplete_aspic.import_export.\
    incomplete_argumentation_theory_from_xlsx_reader import \
    IncompleteArgumentationTheoryFromXLSXFileReader

# Load argumentation system and queryables for the fraud system.
from py_arg.incomplete_aspic.import_export.\
    incomplete_argumentation_theory_to_lp_file_writer import \
    IncompleteArgumentationTheoryToLPFileWriter

asr = IncompleteArgumentationTheoryFromXLSXFileReader()
iat = asr.read_from_xlsx_file(path_to_resources() /
                              'Police_Intake_System_Anon.xlsx')

topic_literals = [
    'FraudArticle326',
    'FraudArticle326E',
    'FraudArticle326ExpertCheckRequired',
    'FraudArticle326EExpertCheckRequired',
    'CivilCase',
    'RejectComplaint',
    'ReferToHallmarkCompany'
]

# Export IAT with empty knowledge base
IncompleteArgumentationTheoryToLPFileWriter().write(
    incomplete_argumentation_theory=iat,
    file_name='0Knr0.pl',
    topic_literals=topic_literals)

# Generate knowledge bases in various sizes
for knowledge_base_size in range(len(iat.positive_queryables) + 1):
    for sample_nr in range(25):
        knowledge_base = []
        knowledge_candidates = iat.queryables.copy()
        extra_knowledge_required = knowledge_base_size
        while extra_knowledge_required > 0:
            knowledge_base_candidates = [
                q for q in iat.queryables
                if all([not k.is_contrary_or_contradictory_of(q) and k != q
                        for k in knowledge_base])]
            if not knowledge_base_candidates:
                raise ValueError(
                    f'Could not make knowledge base of '
                    f'size {str(knowledge_base)} for '
                    f'argumentation system.')
            new_knowledge_base_item = random.choice(knowledge_base_candidates)
            knowledge_base.append(new_knowledge_base_item)
            extra_knowledge_required -= 1

            iat.knowledge_base_axioms = knowledge_base
            IncompleteArgumentationTheoryToLPFileWriter().write(
                incomplete_argumentation_theory=iat,
                file_name=f'{str(knowledge_base_size)}Knr{str(sample_nr)}.pl',
                topic_literals=topic_literals)
