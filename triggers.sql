drop trigger if exists t1_sabervisto on episodios;
create or replace function ft1_obtenervisto() returns trigger language plpgsql as $$
declare

begin

if new.episodios_vistos=old.episodios_totales then
    update contenido set visualizacion='Visto' where codc=old.codc;
elif new.episodios_vistos<old.episodios_totales then
    update contenido set visualizacion='Viendo' where codc=old.codc;
end if;
return new;
end;$$;

create trigger t1_sabervisto after insert on xogador for each row execute procedure ft1_obtenervisto();
