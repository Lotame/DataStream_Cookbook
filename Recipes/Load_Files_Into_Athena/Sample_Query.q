-- Assume we already create DataStream_Sample and Mapping_Sample in Athena
-- Let's run some sample queries in Athena

-- Calculate how many profile add the sport & recreation behavior in the DataStream
Select behavior_path, count(distinct profile_id) cc FROM
Mapping_Sample a
join
DataStream_Sample b
on (a.behavior_id=b.behavior_id)
where
a.behavior_path like 'Lotame Category Hierarchy^Sports & Recreation%' and b.action = 'add'
group by behavior_path order by cc desc;