<template>
    <div>
        <b-navbar toggleable="sm" type="light" variant="light" class="mb-5">
            <b-navbar-toggle target="nav-text-collapse"></b-navbar-toggle>

            <b-navbar-brand>BootstrapVue</b-navbar-brand>
            <b-navbar-nav>
                <b-nav-item>
                    <router-link to="/">Home</router-link>
                </b-nav-item>
                <b-nav-item>
                    <router-link to="/about">About</router-link>
                </b-nav-item>
            </b-navbar-nav>
            <b-navbar-nav class="ml-auto">
                <b-nav-item right>
                    <router-link to="/login">Login</router-link>
                </b-nav-item>
            </b-navbar-nav>
        </b-navbar>
    </div>
</template>

<script>
export default {
    name: "NavigationBar"
}
</script>