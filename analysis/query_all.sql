select
	p.name as file_name,
	m.name as metric,
	l.value as value
from 
	projects p
	inner join live_measures l on p.uuid = l.component_uuid
	inner join metrics m on l.metric_id = m.id
where
	l.metric_id in (3, 18) -- metricas que se deseja extrair do arquivo em questao
	and p."scope" = 'FIL' and p.qualifier = 'FIL'