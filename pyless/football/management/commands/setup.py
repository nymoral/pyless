from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from football.models import Team

class Command(BaseCommand):
    help = 'Insert teams into fresh database'

    teams = {"Afganistanas": "Af", "Airija": "Ie", "Albanija": "Al", "Alžyras": "Dz", "Argentina": "Ar", "Armėnija": "Am", "Australija": "Au", "Austrija": "At", "Azerbaidžanas": "Az", "Baltarusija": "By", "Belgija": "Be", "Bolivija": "Bo", "Bosnija ir Hercogovina": "Ba", "Brazilija": "Br", "Bulgarija": "Bg", "Čekijos Respublika": "Cz", "Čilė": "Cl", "Danija": "Dk", "Didžioji Britanija": "Gb", "Dominikos Sandrauga": "Dm", "Dominikos Respublika": "Do", "Dramblio Kaulo Krantas": "Ci", "Ekvadoras": "Ec", "Egiptas": "Eg", "Estija": "Ee", "Gajana": "Gy", "Gana": "Gh", "Grenlandija": "Gl", "Graikija": "Gr", "Gruzija": "Ge", "Hong Kongas": "Hk", "Hondūras": "Hn", "Indija": "In", "Irakas": "Iq", "Iranas": "Ir", "Islandija": "Is", "Ispanija": "Es", "Italija": "It", "Izraelis": "Il", "Japonija": "Jp", "Jugoslavija": "Y", "Jungtinė Karalystė": "Gb", "Jungtinės Amerikos Valstijos": "Us", "Kanada": "Ca", "Kamerūnas": "Cm", "Kazachstanas": "Kz", "Kinija": "Cn", "Kirgizstanas": "Kg", "Kolumbija": "Co", "Kroatija": "Hr", "Kuba": "Cu", "Kosta Rika": "Cr", "Latvija": "Lv", "Lenkija": "Pl", "Lietuva": "Lt", "Liuksemburgas": "Lu", "Makedonija": "Mk", "Marokas": "Ma", "Meksika": "Mx", "Moldavija": "Md", "Mongolija": "Mn", "Naujoji Zelandija": "Nz", "Nyderlandai": "Nl", "Nigerija": "Ng", "Norvegija": "No", "Paragvajus": "Py", "Per": "Pe", "Pietų Afrika ": "Za", "Pietų Korėja": "Kr", "Portugalija": "Pt", "Prancūzija": "Fr", "Rumunija": "Ro", "Rusija": "Ru", "Singapūras": "Sg", "Slovakija": "Sk", "Slovėnija": "Si", "Surinamas": "Sr", "Suomija": "Fi", "Šiaurės Korėja": "Kp", "Švedija": "Se", "Šveicarija": "Ch", "Tailandas": "Th", "Taivanis": "Tw", "Tadžikistanas": "Tj", "Turkija": "Tr", "Turkmėnija": "Tm", "Ukraina": "Ua", "Urugvajus": "Uy", "Uzbekija": "Uz", "Vatikanas": "Va", "Venesuela": "Ve", "Vengrija": "Hu", "Vietnamas": "Vn", "Vokietija": "De", "Zambija": "Zm"}


    def handle(self, *args, **options):
        c = 0
        for name, code in self.teams.items():
            team = Team(short=code.upper(), full_name=name)
            try:
                team.save(force_insert=True)
            except IntegrityError:
                pass
            else:
                self.stdout.write('{} added'.format(team.short))
                c += 1

        self.stdout.write('{} Teams added'.format(c))
