import json
from infi.clickhouse_orm.database import Database
from infi.clickhouse_orm import models, fields, engines



class InstanceData(models.Model):
	service = fields.NullableField(fields.StringField(default="None"))
	instanceType = fields.NullableField(fields.StringField(default="None"))
	vcpu = fields.NullableField(fields.StringField(default="None"))
	processor = fields.NullableField(fields.StringField(default="None"))
	location = fields.NullableField(fields.StringField(default="None"))
	clockSpeed = fields.NullableField(fields.StringField(default="None"))
	memory = fields.NullableField(fields.StringField(default="None"))
	storage = fields.NullableField(fields.StringField(default="None"))
	networkPerformance = fields.NullableField(fields.StringField(default="None"))
	processorArchitecture = fields.NullableField(fields.StringField(default="None"))
	operatingSystem = fields.NullableField(fields.StringField(default="None"))
	termType = fields.NullableField(fields.StringField(default="None"))
	unit = fields.NullableField(fields.StringField(default="None"))
	pricePerUnit = fields.NullableField(fields.StringField(default="None"))
	engine = engines.Memory()

db = Database('my_test_db')
db.create_table(InstanceData)

fil = open('../tmp.json')
d = json.load(fil)

output = {}

for sku, product in d['products'].items():
	instanceType = product['attributes'].get('instanceType')
	vcpu = product['attributes'].get('vcpu')
	processor = product['attributes'].get('physicalProcessor')
	location = product['attributes'].get('location')
	clockSpeed = product['attributes'].get('clockSpeed')
	memory = product['attributes'].get('memory')
	storage = product['attributes'].get('storage')
	networkPerformance = product['attributes'].get('networkPerformance')
	processorArchitecture = product['attributes'].get('processorArchitecture')
	operatingSystem = product['attributes'].get('operatingSystem')

	try:
		a = d['terms']['OnDemand'].get(sku)
		b = next(iter(a.values()))['priceDimensions']
		unit = next(iter(b.values()))['unit']
	except(KeyError, AttributeError):
		unit = None

	try:
		a = d['terms']['OnDemand'].get(sku)
		b = next(iter(a.values()))['priceDimensions']
		c = next(iter(b.values()))['pricePerUnit']
		pricePerUnit = next(iter(c.values()))
	except(KeyError, AttributeError):
		pricePerUnit = None

	try:
		output[sku].append(sku, instanceType, vcpu, processor, location, clockSpeed, memory, storage, networkPerformance, processorArchitecture, operatingSystem, unit, pricePerUnit)
	except KeyError:
		output[sku] = [sku, instanceType, vcpu, processor, location, clockSpeed, memory, storage, networkPerformance, processorArchitecture, operatingSystem, unit, pricePerUnit]



print(db.count(InstanceData))
qs = InstanceData.objects_in(db)
for instance in qs:
	print(instance)

# for size, lst in output.items():
# 	instance = InstanceData(
# 		service='Amazon', 
# 		instanceType=lst[1],
# 		vcpu=lst[2],
# 		processor=lst[3],
# 		location=lst[4],
# 		clockSpeed=lst[5],
# 		memory=lst[6],
# 		storage=lst[7],
# 		networkPerformance=lst[8],
# 		processorArchitecture=lst[9],
# 		operatingSystem=lst[10],
# 		termType='OnDemand',
# 		unit=lst[11],
# 		pricePerUnit=lst[12]
# 	)
# 	db.insert([instance])