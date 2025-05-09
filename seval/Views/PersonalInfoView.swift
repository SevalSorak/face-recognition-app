import SwiftUI

struct PersonalInfoView: View {
    let person: Person?

    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("Kişisel Bilgiler")
                .font(.largeTitle)
                .bold()
                .padding(.horizontal)
                .padding(.top)

            if let person = person {
                Group {
                    InfoRow(title: "Ad", value: person.firstName)
                    InfoRow(title: "Soyad", value: person.lastName)
                    InfoRow(title: "Yaş", value: "\(person.age)")
                    InfoRow(title: "Cinsiyet", value: person.gender)
                    InfoRow(title: "Meslek", value: person.occupation)
                    InfoRow(title: "Telefon", value: person.phoneNumber)
                    InfoRow(title: "E-posta", value: person.email)
                }

                Spacer()

                Button(action: {
                    // Kişisel bilgileri düzenleme işlemi
                }) {
                    Text("Bilgileri Düzenle")
                        .font(.system(size: 16, weight: .semibold))
                        .foregroundColor(.white)
                        .padding()
                        .frame(maxWidth: .infinity)
                        .background(
                            LinearGradient(
                                gradient: Gradient(colors: [.blue, .purple]),
                                startPoint: .leading,
                                endPoint: .trailing
                            )
                        )
                        .clipShape(RoundedRectangle(cornerRadius: 10))
                        .shadow(color: .black.opacity(0.1), radius: 5, x: 0, y: 3)
                }
                .padding(.horizontal)
                .padding(.bottom)
            } else {
                Text("Kişi tanınmadı")
                    .font(.headline)
                    .foregroundColor(.gray)
                    .padding(.horizontal)

                Spacer()
            }
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Color(UIColor.systemBackground))
        .clipShape(RoundedRectangle(cornerRadius: 12))
        .shadow(color: .black.opacity(0.05), radius: 8, x: 0, y: 4)
    }
}

// MARK: - InfoRow

struct InfoRowNew: View {
    let title: String
    let value: String

    var body: some View {
        HStack {
            Text(title)
                .font(.system(size: 16, weight: .medium))
                .foregroundColor(.secondary)
                .frame(width: 100, alignment: .leading)

            Text(value)
                .font(.system(size: 16))
                .foregroundColor(.primary)
                .frame(maxWidth: .infinity, alignment: .leading)
        }
        .padding(.vertical, 8)
        .padding(.horizontal, 12)
        .background(Color(UIColor.secondarySystemBackground))
        .clipShape(RoundedRectangle(cornerRadius: 8))
        .padding(.horizontal)
    }
}
