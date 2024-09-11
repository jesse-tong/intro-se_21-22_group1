<template>
    <div class="about">
        <h1>About Page</h1>
        <h2>Attribution</h2>
        <ul>
            <li>
                <strong>DB-IP:</strong> This project uses the DB-IP database for IP geolocation. Visit their website at <a href="https://db-ip.com/">https://db-ip.com/</a> for more information.
            </li>
            <li>
                <strong>OpenStreetMap:</strong> This project uses OpenStreetMap for displaying maps. Visit their website at <a href="https://www.openstreetmap.org/">https://www.openstreetmap.org/</a> for more information.
            </li>
            <li>
                <strong>Chart.js:</strong> This project uses Chart.js for displaying charts. Visit their website at <a href="https://www.chartjs.org/">https://www.chartjs.org/</a> for more information.
            </li>
            <li>
                <strong>game-icons.net</strong> This project uses icons from game-icons.net. Visit their website at <a href="https://game-icons.net/">https://game-icons.net/</a> for more information.
            </li>
        </ul>
    </div>
</template>

<script>
export default {
    name: 'About',
};
</script>

<style scoped>
.about {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}
</style>