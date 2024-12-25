/**
Informo que lo que hay desarrollado de programa todavia no esta adaptado para algunas de las cosas que se han definido aqui
por eso insto a colaborar ya que es un desarrollo grande
**/
DO $$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_database WHERE datname = 'contenido_audiovisual'
   ) THEN
      PERFORM pg_create_physical_replication_slot('contenido_audiovisual');
   END IF;
END
$$;

