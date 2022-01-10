from django.shortcuts import render
from django.db import connection
from .models import Pokemon

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


# Create your views here.
def home(request):
    return render(request, 'home.html')


def query():
    with connection.cursor() as cursor:
        cursor.execute("""
        select Generation, Name
        from Pokemons as P1
        where
            Legendary = 1
          and
            HP + Attack + Defense >= all(
                  select P2.HP + P2.Attack + P2.Defense
                  from Pokemons as P2
                  where P2.Generation = P1.Generation
                )
        order by Generation asc;
        """)
        sql_res1 = dictfetchall(cursor)
        cursor.execute("""
        select Type, Name
        from Pokemons as P
        where
            HP > all(
                select P2.HP
                from Pokemons as P2
                where P2.Type = P.Type
                and not P2.Name = P.Name
                )
        and
            Attack > all(
                select P2.Attack
                from Pokemons as P2
                where P2.Type = P.Type
                and not P2.Name = P.Name
                )
        and
            Defense > all(
                select P2.Defense
                from Pokemons as P2
                where P2.Type = P.Type
                and not P2.Name = P.Name
                )
        order by Type asc;
             """)
        sql_res2 = dictfetchall(cursor)
        cursor.execute("""
        select Type, round(average_instability, 2) as av_instability
        from (
            select Type, avg(CAST(abs(Defense - Attack) AS FLOAT)) as average_instability
            from Pokemons
            group by Type
        ) avg_inst_table
        where average_instability >= all(
            select avg(CAST(abs(Defense - Attack) AS FLOAT))
            from Pokemons
            group by Type
            );
                     """)
        sql_res3 = dictfetchall(cursor)
    return sql_res1, sql_res2, sql_res3


def query_results(request):
    sql_res1, sql_res2, sql_res3 = query()
    return render(request, 'query_results.html', {'sql_res1': sql_res1, 'sql_res2': sql_res2,
                                                  'sql_res3': sql_res3, 'sql_res4': []})


def run_query(request):
    sql_res1, sql_res2, sql_res3 = query()
    attack_threshold = request.POST['attack_threshold']
    pokemon_count = request.POST['pokemon_count']
    with connection.cursor() as cursor:
        cursor.execute(f"""
        select distinct countTable.Type as countType
        from (select Type, count(*) pokemon_count
            from Pokemons
            group by Type
            ) countTable
        inner join
            (select Type
            from Pokemons
            where Attack > {attack_threshold}
            ) attackTable
        on countTable.Type = attackTable.Type
        where pokemon_count > {pokemon_count}
        """)
        sql_res4 = dictfetchall(cursor)
    return render(request, 'query_results.html', {'sql_res1': sql_res1, 'sql_res2': sql_res2,
                                                  'sql_res3': sql_res3, 'sql_res4': sql_res4})


def add_pokemon(request):
    return render(request, 'add_pokemon.html')


def add(request):
    poke_name=request.POST['name']
    poke_type=request.POST['type']
    poke_gen=request.POST['gen']
    poke_status=request.POST.get('legendary',False)
    poke_hp=request.POST['hp']
    poke_attack=request.POST['atk']
    poke_defense=request.POST['def']
    new_pokemon = Pokemon(Name=poke_name,Type=poke_type,Generation=poke_gen,Legendary=poke_status,Hp=poke_hp,Attack=poke_attack,Defense=poke_defense)
    new_pokemon.save()
    return render(request, 'add_pokemon.html')

