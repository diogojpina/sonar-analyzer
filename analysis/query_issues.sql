select
	i.kee as uuid,
	i.severity,
	i.message as message,
	i.line as line,
	p.name as file_name,
	m.name as metric,
	l.value as value
from
	issues i 
	inner join projects p on i.component_uuid = p.uuid
	inner join live_measures l on i.component_uuid = l.component_uuid
	inner join metrics m on l.metric_id = m.id
where
	-- uuid's das dívidas técnicas com tipo BLOCKER ou CRITICAL
	i.severity in ('BLOCKER', 'CRITICAL')
	and l.metric_id in (3, 18) -- metricas que se deseja extrair do arquivo em questao