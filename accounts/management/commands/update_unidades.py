from django.core.management.base import BaseCommand
from chamados.models import Unidade


class Command(BaseCommand):
    help = 'Atualiza as unidades do sistema'

    def handle(self, *args, **options):
        # Lista de unidades a serem criadas
        unidades = [
            'Vila Ideal',
            'STC',
            'TAMOIO ADM',
            'TAMOIO LABORATÓRIO',
            'ARNÃO ADM',
            'ZECA LAB',
            'ZECA ADM',
            'CENTENÁRIO ADM',
            'CENTENÁRIO LAB',
            'VILA OPRÁRIA LAB',
            'VILA OPERÁRIA ADM',
            'LAUREANO LAB',
            'LAUREANO ADM',
            'CHACRINHA LAB',
            'CHACRINHA ADM',
            'PARQUE DAS MISSÕES RECEP',
            'PARQUE DAS MISSÕES LAB',
            'JARDIM GRAMACHO ADM',
            'JARDIM GRAMACHO LAB',
            'CEDERJ LAB',
            'CEDERJ DIRETORIA',
            'POLO DA BELEZA ADM',
            'POLO DA BELEZA ADM2',
            'PQ LAFAETE ADM',
            'PQ LAFAETE LAB',
            'POLO SOCIAL RECEP',
            'POLO SOCIAL ADM ENFER',
            'POLO SOCIAL LAB',
            'POLO SOCIAL JULIANA',
            'CASA BRASIL LAB',
            'CASA BRASIL ADM',
            'CAPIVARI ADM',
            'CAPIVARI LAB',
            'PANTANAL ADM',
            'PANTANAL LAB',
            'FIGUEIRA LAB',
            'FIGUEIRA ADM',
            'PQ ANADANTAS LAB',
            'PQ ANADANTAS ADM',
            'JD PRIMAVERA LAB',
            'JD PRIMAVERA ADM',
            'ASSECAMP ADM',
            'CORTE 8 ADM',
            'CORTE 8 LAB',
            'INCLUSÃO ADM',
            'LAGUNAS ADM',
            'BERRABOI LAB',
            'BERRABOI ADM',
            'IG WESLEYANA ADM',
            'SONINHA(PILAR) ADM',
            'SONINHA(PILAR) LAB',
            'GRAMACHO LAB',
            'GRAMACHO MRC',
            'GRAMACHO ADM',
            'GRAMACHO PRE ENEM',
            'GRAMACHO SALA ELETRICA',
            'PQ FELICIDADE',
            'PERIQUITOS',
            'DECIMO QUINTO',
            'PQ VILA NOVA',
            'PROJETO VQQ',
            'SEDE',
        ]

        self.stdout.write('🔄 Atualizando unidades...\n')

        # Remover unidades de teste que não estão na nova lista
        unidades_existentes = Unidade.objects.all()
        unidades_para_manter = set(unidades)
        
        removidas = 0
        for unidade in unidades_existentes:
            if unidade.nome not in unidades_para_manter:
                # Verificar se a unidade tem perfis ou chamados associados
                tem_perfis = unidade.profiles.exists()
                tem_chamados = unidade.chamados.exists()
                
                if tem_perfis or tem_chamados:
                    self.stdout.write(
                        self.style.WARNING(
                            f'⚠️  Mantendo "{unidade.nome}" (possui perfis ou chamados associados)'
                        )
                    )
                else:
                    unidade.delete()
                    removidas += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Removida: {unidade.nome}')
                    )

        # Criar novas unidades
        criadas = 0
        ja_existentes = 0
        for nome_unidade in unidades:
            unidade, created = Unidade.objects.get_or_create(nome=nome_unidade)
            if created:
                criadas += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Criada: {nome_unidade}')
                )
            else:
                ja_existentes += 1

        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS(f'✅ Processo concluído!'))
        self.stdout.write(f'   📊 Resumo:')
        self.stdout.write(f'      • Unidades criadas: {criadas}')
        self.stdout.write(f'      • Unidades já existentes: {ja_existentes}')
        self.stdout.write(f'      • Unidades removidas: {removidas}')
        self.stdout.write(f'      • Total de unidades: {Unidade.objects.count()}')
        self.stdout.write('=' * 60 + '\n')
