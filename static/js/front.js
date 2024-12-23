
        // Canvas setup and animation
        const canvas = document.getElementById('geometric-bg');
        const ctx = canvas.getContext('2d');

        // Set canvas size
        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }

        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);

        // Triangle class for better organization
        class Triangle {
            constructor(x, y, size) {
                this.x = x;
                this.y = y;
                this.size = size;
                this.angle = Math.random() * Math.PI * 2;
                this.speed = 0.001 + Math.random() * 0.002;
                this.color = this.generateColor();
            }

            generateColor() {
                const colors = [
                    'rgba(236, 72, 153, 0.3)',  // Pink
                    'rgba(147, 51, 234, 0.3)',  // Purple
                    'rgba(59, 130, 246, 0.3)',  // Blue
                    'rgba(249, 115, 22, 0.3)',  // Orange
                ];
                return colors[Math.floor(Math.random() * colors.length)];
            }

            update() {
                this.angle += this.speed;
                this.x += Math.cos(this.angle) * 0.2;
                this.y += Math.sin(this.angle) * 0.2;
            }

            draw() {
                ctx.beginPath();
                ctx.moveTo(
                    this.x + Math.cos(this.angle) * this.size,
                    this.y + Math.sin(this.angle) * this.size
                );
                ctx.lineTo(
                    this.x + Math.cos(this.angle + 2.0944) * this.size,
                    this.y + Math.sin(this.angle + 2.0944) * this.size
                );
                ctx.lineTo(
                    this.x + Math.cos(this.angle + 4.1888) * this.size,
                    this.y + Math.sin(this.angle + 4.1888) * this.size
                );
                ctx.closePath();
                ctx.fillStyle = this.color;
                ctx.fill();
            }
        }

        // Create triangles
        const triangles = [];
        const triangleCount = 50;

        for (let i = 0; i < triangleCount; i++) {
            const x = Math.random() * canvas.width;
            const y = Math.random() * canvas.height;
            const size = 50 + Math.random() * 100;
            triangles.push(new Triangle(x, y, size));
        }

        // Animation loop
        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Create gradient background
            const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
            gradient.addColorStop(0, '#f97316');  // Orange
            gradient.addColorStop(0.5, '#a855f7'); // Purple
            gradient.addColorStop(1, '#3b82f6');  // Blue
            ctx.fillStyle = gradient;
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Update and draw triangles
            triangles.forEach(triangle => {
                triangle.update();
                triangle.draw();
            });

            requestAnimationFrame(animate);
        }

        animate();

        // Interactive elements
        document.querySelector('.create-btn').addEventListener('click', () => {
            alert('Please log in to create an event!');
        });

        // Smooth scroll for navigation links
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const href = link.getAttribute('href');
                document.querySelector(href)?.scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });
   