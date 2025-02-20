drop trigger if exists t1_sabervisto on episodios;
create or replace function ft1_obtenervisto() returns trigger language plpgsql as $$
declare

begin



return new;
end;$$;

create trigger t1_sabervisto after insert on xogador for each row execute procedure ft1_obtenervisto();
