def bayes_spam_probability(total_emails, free_emails, spam_emails, spam_and_free_emails):
    # Probabilities
    p_spam = spam_emails / total_emails
    p_free = free_emails / total_emails
    p_free_given_spam = spam_and_free_emails / spam_emails

    # Bayes' Theorem
    p_spam_given_free = (p_free_given_spam * p_spam) / p_free

    return p_spam_given_free

# Given data
total_emails = 1000
free_emails = 300
spam_emails = 400
spam_and_free_emails = 120

# Calculate
result = bayes_spam_probability(total_emails, free_emails, spam_emails, spam_and_free_emails)
print(f"P(Spam | Free): {result:.4f}")
