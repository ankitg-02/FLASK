// Contact form validation and fake submission
const form = document.getElementById('contactForm');
const formMessage = document.getElementById('formMessage');

if (form) {
    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const name = document.getElementById('name').value.trim();
        const email = document.getElementById('email').value.trim();
        const message = document.getElementById('message').value.trim();

        if (name && email && message) {
            formMessage.textContent = 'Thank you for your message! I will get back to you soon.';
            form.reset();
        } else {
            formMessage.textContent = 'Please fill out all fields.';
        }
    });
}

// Optional: Load dynamic blog posts (static example)
const posts = document.getElementById('posts');

if (posts) {
    const samplePosts = [
        { title: 'Understanding JavaScript Basics', summary: 'Learn the fundamentals of JavaScript.', link: '#' },
        { title: 'Tips for Effective Blogging', summary: 'Improve your blog writing with these tips.', link: '#' }
    ];

    samplePosts.forEach(post => {
        const article = document.createElement('article');
        article.innerHTML = `
      <h3>${post.title}</h3>
      <p>${post.summary}</p>
      <a href="${post.link}">Read More</a>
    `;
        posts.appendChild(article);
    });
}
