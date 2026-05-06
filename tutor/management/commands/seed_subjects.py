from django.core.management.base import BaseCommand
from tutor.models import Subject

class Command(BaseCommand):
    help = 'Seed default subjects into the database'

    def handle(self, *args, **kwargs):
        subjects = [
            ("Mathematics", "Algebra, Calculus, Geometry and more"),
            ("Physics", "Mechanics, Thermodynamics, Electromagnetism"),
            ("Chemistry", "Organic, Inorganic and Physical Chemistry"),
            ("Biology", "Cell Biology, Genetics, Human Anatomy"),
            ("Computer Science", "Programming, Data Structures, Algorithms"),
            ("English", "Grammar, Writing, Literature"),
            ("History", "World History, Modern History"),
            ("Geography", "Physical and Human Geography"),
            ("Economics", "Micro and Macroeconomics"),
            ("Accountancy", "Financial Accounting, Cost Accounting"),
            ("Python Programming", "Core Python, Django, Data Science"),
            ("Web Development", "HTML, CSS, JavaScript, React"),
        ]

        created = 0
        for name, desc in subjects:
            obj, made = Subject.objects.get_or_create(name=name, defaults={'description': desc})
            if made:
                created += 1
                self.stdout.write(self.style.SUCCESS(f'  Added: {name}'))
            else:
                self.stdout.write(f'  Already exists: {name}')

        self.stdout.write(self.style.SUCCESS(f'Done! {created} new subjects added.'))
