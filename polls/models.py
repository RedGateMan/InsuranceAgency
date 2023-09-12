from django.db import models

from polls.constants import INSURANCE_TYPE, OBJECT_TYPE, STATUS, SALARY
from MyAuth.models import User


# Create your models here.


class Office(models.Model):
	name = models.CharField(max_length=30)
	address = models.CharField(max_length=50)
	phone = models.CharField(max_length=13)

	def __str__(self):
		return f'[#{self.id}] {self.name}'


class Insurance(models.Model):
	insurance_type = models.CharField(
		max_length=20,
		default="GEN",
		choices=INSURANCE_TYPE
	)
	minimal_cost = models.IntegerField()
	duration = models.DurationField()
	percentage = models.FloatField()

	def __str__(self):
		return f'[#{self.id}] Type: {self.insurance_type}, Duration: {self.duration}'


class Object(models.Model):
	object_type = models.CharField(
		max_length=20,
		choices=OBJECT_TYPE
	)
	description = models.TextField()

	def __str__(self):
		return f'[#{self.id}] Type: {self.object_type}'


class Agent(models.Model):
	office = models.ForeignKey(
		to=Office,
		null=True,
		on_delete=models.SET_NULL,
	)
	user = models.OneToOneField(
		to=User,
		limit_choices_to={"is_staff": True},
		null=True,
		on_delete=models.CASCADE,

	)

	def get_salary(self):
		contracts = Contract.objects.filter(agent_id=self.id, status='ACTIVE')
		salary = 0
		for contract in contracts:
			if contract.cost is not None:
				salary += float(contract.cost) * contract.insurance.percentage
			else:
				return 0
		return salary * SALARY

	def __str__(self):
		return f'[#{self.id}] {self.user.name + " " + self.user.surname}, Office: {self.office.name}'


class Contract(models.Model):
	status = models.CharField(
		max_length=15,
		default="PENDING",
		null=True,
		blank=True,
		choices=STATUS,
	)
	client = models.ForeignKey(
		to=User,
		null=True,
		blank=True,
		on_delete=models.CASCADE,
	)
	agent = models.ForeignKey(
		to=Agent,
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
	)
	insurance = models.ForeignKey(
		to=Insurance,
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
	)
	object = models.OneToOneField(
		to=Object,
		null=True,
		blank=True,
		on_delete=models.CASCADE,
	)
	sign_date = models.DateTimeField(auto_now_add=True)
	cost = models.CharField(
		null=True,
		blank=True,
		max_length=60
	)

	def __str__(self):
		return f'[#{self.id}] Client: {self.client.surname}, Agent: {self.agent.user.surname}, ' \
			   f'Object: {self.object.object_type} -- {self.object.description}'
