from regulon_summary.cli import parse_arguments
from regulon_summary.core import build_regulon
from regulon_summary.exporters import write_sif, write_summary
from regulon_summary.filters import (
    filter_by_min_genes,
    filter_by_type,
    filter_interactions_by_regulon,
)
from regulon_summary.io import load_interactions


def main():
    args = parse_arguments()

    if args.min_genes < 0:
        print("Error: min_genes debe ser mayor o igual a 0.")
        raise SystemExit(1)

    if args.top_n <= 0:
        print("Error: top_n debe ser mayor que 0.")
        raise SystemExit(1)

    interactions = load_interactions(args.input_file)

    if interactions.empty:
        print("Advertencia: no se encontraron interacciones válidas.")

    regulon = build_regulon(interactions)

    regulon = filter_by_min_genes(regulon, args.min_genes)
    regulon = filter_by_type(regulon, args.type)

    if regulon.empty:
        print("Advertencia: no hay reguladores que cumplan el filtro.")

    if args.format == "summary":
        write_summary(regulon, args.output_file, top_n=args.top_n)
    else:
        filtered_interactions = filter_interactions_by_regulon(
            interactions,
            regulon,
        )
        write_sif(filtered_interactions, args.output_file)

    if args.plot == "top_regulators":
        plot_top_regulators(
            regulon,
            args.plot_file,
            top_n=args.top_n,
        )

    elif args.plot == "type_distribution":
        plot_type_distribution(
            regulon,
            args.plot_file,
        )

    print(f"Archivo generado: {args.output_file}")

    if args.plot != "none":
        print(f"Gráfica generada: {args.plot_file}")



if __name__ == "__main__":
    main()
