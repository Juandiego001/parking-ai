<template>
    <v-data-table :items="items" :headers="headers" :items-per-page="perPage" @update:itemsPerPage="v => perPage = v">
        <template v-slot:item.options="{ item }">
            <v-btn color="blue-darken-4" variant="icon" icon="mdi-pencil" @click="setUpdate(item.id)"></v-btn>
            <v-btn color="red-darken-4" variant="icon" icon="mdi-trash-can"
                @click="form = item; deleteDialog = true"></v-btn>
        </template>
    </v-data-table>

    <!-- Update Dialog -->
    <v-dialog v-model="updateDialog" max-width="500">
        <v-card>
            <v-card-title class="bg-blue-darken-4">
                <v-row no-gutters align="center">
                    Update Vehicle
                    <v-spacer></v-spacer>
                    <v-btn class="bg-blue-darken-4" variant="icon" icon="mdi-close"
                        @click="updateDialog = false"></v-btn>
                </v-row>
            </v-card-title>
            <v-card-text>
                <v-form @submit.prevent="updateVehicle">
                    <v-row>
                        <v-col cols="6">
                            <v-select v-model="form.apartmentId" :items="apartments" item-title="unit" item-value="id"
                                color="blue-darken-4" label="Apartment" hide-details="auto"></v-select>
                        </v-col>
                        <v-col cols="6">
                            <v-text-field v-model="form.plate" color="blue-darken-4" label="Plate"
                                hide-details="auto"></v-text-field>
                        </v-col>
                        <v-col cols="12">
                            <v-text-field v-model="form.description" color="blue-darken-4" label="Description"
                                hide-details="auto"></v-text-field>
                        </v-col>
                        <v-col cols="12" class="text-end">
                            <v-btn color="blue-darken-4" variant="outlined" @click="updateDialog = false">Cancel</v-btn>
                            <span class="mx-1"></span>
                            <v-btn type="submit" class="bg-blue-darken-4">Create</v-btn>
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
                    Register New Vehicle
                    <v-spacer></v-spacer>
                    <v-btn class="bg-blue-darken-4" variant="icon" icon="mdi-close"
                        @click="createDialog = false"></v-btn>
                </v-row>
            </v-card-title>
            <v-card-text>
                <v-form @submit.prevent="createVehicle">
                    <v-row>
                        <v-col cols="6">
                            <v-select v-model="form.apartmentId" :items="apartments" item-title="unit" item-value="id"
                                color="blue-darken-4" label="Apartment" hide-details="auto"></v-select>
                        </v-col>

                        <v-col cols="6">
                            <v-text-field v-model="form.plate" color="blue-darken-4" label="Plate"
                                hide-details="auto"></v-text-field>
                        </v-col>

                        <v-col cols="12">
                            <v-text-field v-model="form.description" color="blue-darken-4" label="Description"
                                hide-details="auto"></v-text-field>
                        </v-col>

                        <v-col cols="12" class="text-end">
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
                    Delete Vehicle
                    <v-spacer></v-spacer>
                    <v-btn class="bg-red-darken-4" variant="icon" icon="mdi-close"
                        @click="deleteDialog = false"></v-btn>
                </v-row>
            </v-card-title>
            <v-card-text>
                <v-form @submit.prevent="deleteVehicle">
                    <v-row>
                        <v-col cols="12">
                            Are you sure you want to delete the Vehicle {{ form.plate }}?
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
                    Search Vehicle
                    <v-spacer></v-spacer>
                    <v-btn class="bg-blue-darken-4" variant="icon" icon="mdi-close"
                        @click="searchDialog = false"></v-btn>
                </v-row>
            </v-card-title>
            <v-card-text>
                <v-form>
                    <v-row>
                        <v-col cols="12">
                            <v-text-field v-model="search" label="Plate"></v-text-field>
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
        apartments: [],
        items: [],
        search: '',
        page: 1,
        perPage: 15,
        form: {
            id: '',
            plate: '',
            description: '',
            apartmentId: '',
            status: '',
            created_at: '',
            updated_at: ''
        },
        updateDialog: false,
        deleteDialog: false
    }),
    computed: {
        headers() {
            return [
                { title: 'Id', key: 'id' },
                { title: 'Plate', key: 'plate' },
                { title: 'Apartment', key: 'apartmentId' },
                { title: 'Status', key: 'status' },
                { title: 'Options', key: 'options', align: 'center' }
            ]
        }
    },
    watch: {
        async createDialog(val) {
            if (val) {
                await this.getApartments()
                this.form = {
                    plate: '',
                    description: '',
                    apartmentId: ''
                }
            }
        }
    },
    async beforeMount() {
        await this.getVehicles()
    },
    methods: {
        async getApartments() {
            try {
                const { items } = await $fetch('/api/apartments/', { method: 'GET' })
                this.apartments = items
            } catch (err) {
                console.log(err)
            }
        },
        async getVehicles() {
            try {
                const { items } = await $fetch('/api/vehicles/', {
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
        async createVehicle() {
            try {
                const { message } = await $fetch('/api/vehicles/', {
                    method: 'POST',
                    body: this.form
                })
                console.log('RESPONSE: ', message);
                await this.getVehicles();
				this.createDialog = false;
            } catch (err) {
                console.log(err);
            }
        },
        async setUpdate(vehicleId) {
            try {
                this.form = await $fetch(`/api/vehicles/${vehicleId}`, {
                    method: 'GET'
                })
                this.updateDialog = true
            } catch (err) {
                console.log(err);
            }
        },
        async updateVehicle() {
            try {
                const response = await $fetch(`/api/vehicles/${this.form.id}`, {
                    method: 'PUT',
                    body: this.form
                })
                console.log('RESPONSE UPDATE: ');
                console.log(response);
                await this.getVehicles()
                this.updateDialog = false;
            } catch (err) {
                console.log(err);
            }
        },
        async deleteVehicle() {
            try {
                const response = await $fetch(`/api/vehicles/${this.form.id}`, { method: 'DELETE' })
                console.log('RESPONSE DELETE: ');
                console.log(response);
                await this.getVehicles()
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