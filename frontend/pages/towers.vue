<template>
	<v-data-table :items="items" :headers="headers" :items-per-page="perPage" @update:itemsPerPage="v => perPage = v">
		<template v-slot:item.options="{ item }">
			<v-btn color="blue-darken-4" variant="icon" icon="mdi-pencil" @click="setUpdate(item.id)"></v-btn>
			<v-btn color="red-darken-4" variant="icon" icon="mdi-trash-can" @click="form = item; deleteDialog = true"></v-btn>
		</template>
	</v-data-table>

	<!-- Update Dialog -->
	<v-dialog v-model="updateDialog" max-width="500">
		<v-card>
			<v-card-title class="bg-blue-darken-4">
				<v-row no-gutters align="center">
					Update Tower
					<v-spacer></v-spacer>
					<v-btn class="bg-blue-darken-4" variant="icon" icon="mdi-close" @click="updateDialog = false"></v-btn>
				</v-row>
			</v-card-title>
			<v-card-text>
				<v-form ref="updateForm" @submit.prevent="updateTower">
					<v-row>
						<v-col cols="6">
							<v-text-field v-model="form.unit" color="blue-darken-4" label="Tower" hide-details="auto"></v-text-field>
						</v-col>

						<v-col cols="6">
							<v-text-field v-model="form.floors" type="number" color="blue-darken-4" label="Floors"
								hide-details="auto"></v-text-field>
						</v-col>

						<v-col class="text-end" cols="12">
							<v-btn color="blue-darken-4" variant="outlined" @click="updateDialog = false">Cancel</v-btn>
							<span class="mx-1"></span>
							<v-btn type="submit" class="bg-blue-darken-4">Update</v-btn>
						</v-col>
					</v-row>
				</v-form>
			</v-card-text>
		</v-card>
	</v-dialog>

	<!-- Create Dialog -->
	<v-dialog v-model="createDialog" max-width="500">
		<v-card>
			<v-card-title class="bg-blue-darken-4">
				<v-row no-gutters align="center">
					Register New Tower
					<v-spacer></v-spacer>
					<v-btn class="bg-blue-darken-4" variant="icon" icon="mdi-close" @click="createDialog = false"></v-btn>
				</v-row>
			</v-card-title>
			<v-card-text>
				<v-form @submit.prevent="createTower">
					<v-row>
						<v-col cols="6">
							<v-text-field v-model="form.unit" color="blue-darken-4" label="Tower" hide-details="auto"></v-text-field>
						</v-col>

						<v-col cols="6">
							<v-text-field v-model="form.floors" color="blue-darken-4" label="Floors"
								hide-details="auto"></v-text-field>
						</v-col>

						<v-col class="text-end" cols="12">
							<v-btn color="blue-darken-4" variant="outlined" @click="updateDialog = false">Cancel</v-btn>
							<span class="mx-1"></span>
							<v-btn type="submit" class="bg-blue-darken-4">Create</v-btn>
						</v-col>
					</v-row>
				</v-form>
			</v-card-text>
		</v-card>
	</v-dialog>

	<!-- Delete Dialog -->
	<v-dialog v-model="deleteDialog" max-width="500">
		<v-card>
			<v-card-title class="bg-red-darken-4">
				<v-row no-gutters align="center">
					Delete Tower
					<v-spacer></v-spacer>
					<v-btn class="bg-red-darken-4" variant="icon" icon="mdi-close" @click="deleteDialog = false"></v-btn>
				</v-row>
			</v-card-title>
			<v-card-text>
				<v-form>
					<v-row>
						<v-col cols="12">
							Are you sure you want to delete the Tower {{ form.unit }}?
						</v-col>
						<v-col class="text-end">
							<v-btn color="red-darken-4" variant="outlined" @click="deleteDialog = false">Cancel</v-btn>
							<span class="mx-1"></span>
							<v-btn type="submit" class="bg-red-darken-4">Delete</v-btn>
						</v-col>
					</v-row>
				</v-form>
			</v-card-text>
		</v-card>
	</v-dialog>

	<!-- Search Dialog -->
	<v-dialog v-model="searchDialog" max-width="500">
		<v-card>
			<v-card-title class="bg-blue-darken-4">
				<v-row no-gutters align="center">
					Search Tower
					<v-spacer></v-spacer>
					<v-btn class="bg-blue-darken-4" variant="icon" icon="mdi-close" @click="searchDialog = false"></v-btn>
				</v-row>
			</v-card-title>
			<v-card-text>
				<v-form @submit.prevent="doSearch">
					<v-row>
						<v-col cols="12">
							<v-text-field v-model="search" label="Tower" hide-details="auto" clearable></v-text-field>
						</v-col>

						<v-col class="text-end" cols="12">
							<v-btn color="blue-darken-4" variant="outlined" @click="updateDialog = false">Cancel</v-btn>
							<span class="mx-1"></span>
							<v-btn type="submit" class="bg-blue-darken-4">Search</v-btn>
						</v-col>
					</v-row>
				</v-form>
			</v-card-text>
		</v-card>
	</v-dialog>
</template>

<script>
import { toRefs } from 'vue'
import { search } from '~/mixins/search'
import { create } from '~/mixins/create'

definePageMeta({
	layout: 'app'
})

export default {
	setup() {
		return {
			...toRefs(search),
			...toRefs(create)
		}
	},
	data: () => ({
		items: [],
		search: '',
		page: 1,
		perPage: 15,
		form: {
			id: '',
			unit: '',
			floors: '',
			status: '',
			createdAt: '',
			updatedAt: ''
		},
		updateDialog: false,
		deleteDialog: false
	}),
	computed: {
		headers() {
			return [
				{ title: 'Id', key: 'id', align: 'center' },
				{ title: 'Tower', key: 'unit' },
				{ title: 'Floors', key: 'floors' },
				{ title: 'Status', key: 'status' },
				{ title: 'Options', key: 'options', align: 'center' }
			]
		}
	},
	watch: {
		createDialog(val) {
			if (val) {
				this.form = {
					unit: '',
					floors: ''
				}
			}
		}
	},
	async beforeMount() {
		await this.getTowers()
	},
	methods: {
		async getTowers() {
			try {
				const { items } = await $fetch('/api/towers/', {
					method: 'GET',
					query: {
						search: this.search,
						page: this.page,
						perPage: this.perPage
					}
				})
				this.items = items
			} catch (err) {
				console.log(err)
			}
		},
		async createTower() {
			try {
				const { message } = await $fetch('/api/towers/', {
					method: 'POST',
					body: this.form
				})
				console.log(message);
				await this.getTowers();
				this.createDialog = false;
			} catch (err) {
				console.log(err);
			}
		},
		async setUpdate(towerId) {
			try {
				this.form = await $fetch(`/api/towers/${towerId}`, {
					method: 'GET'
				})
				this.updateDialog = true
			} catch (err) {
				console.log(err);
			}
		},
		async updateTower() {
			try {
				const response = await $fetch(`/api/towers/${this.form.id}`, {
					method: 'PUT',
					body: this.form
				})
				console.log('RESPONSE UPDATE: ');
				console.log(response);
				await this.getTowers()
				this.updateDialog = false;
			} catch (err) {
				console.log(err);
			}
		},
		async deleteTower() {
			try {
				const response = await $fetch(`/api/towers/${this.form.id}`, { method: 'DELETE' })
				console.log('RESPONSE DELETE: ');
				console.log(response);
				await this.getTowers()
				this.deleteDialog = false
			} catch (err) {
				console.log(err)
			}
		},
		async doSearch() {
			await this.getTowers();
			this.searchDialog = false;
		}
	}
}
</script>